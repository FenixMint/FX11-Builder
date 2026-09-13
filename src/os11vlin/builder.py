from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import tempfile

from . import __version__
from .iso import BuilderError, Edition, IsoInspection, inspect_iso, run_checked, sha256_file
from .profiles import get_profile, validate_profile
from .provisioning import write_provisioning_files


@dataclass(frozen=True)
class BuildResult:
    output_iso: Path
    checksum_file: Path
    output_sha256: str
    source_sha256: str
    edition: Edition
    profiles: tuple[str, ...]


def _validate_profiles(profile_ids: list[str]) -> None:
    if not profile_ids:
        raise BuilderError("At least one profile must be selected.")
    for profile_id in profile_ids:
        validate_profile(get_profile(profile_id))


def export_selected_edition(inspection: IsoInspection, edition: Edition, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    run_checked([
        "wimlib-imagex",
        "export",
        str(inspection.install_image),
        str(edition.index),
        str(destination),
        edition.name,
        edition.description or edition.name,
        "--compress=LZX",
        "--check",
    ])
    run_checked(["wimlib-imagex", "verify", str(destination)])
    return destination


def _manifest(inspection: IsoInspection, edition: Edition, profile_ids: list[str]) -> dict[str, object]:
    return {
        "project": "OS11vLIN",
        "builder_version": __version__,
        "build_utc": datetime.now(timezone.utc).isoformat(),
        "source_iso": inspection.source.name,
        "source_sha256": inspection.source_sha256,
        "source_install_format": inspection.install_format,
        "edition": {
            "source_index": edition.index,
            "name": edition.name,
            "edition_id": edition.edition_id,
            "architecture": edition.architecture,
        },
        "profiles": profile_ids,
        "strategy": {
            "edition": "selected image exported with wimlib to a single-image install.wim",
            "debloat": "Windows SetupComplete removes declared provisioned AppX packages using Windows servicing APIs",
            "privacy": "machine/default-user policy applied during SetupComplete",
            "boot": "original ISO boot metadata replayed by xorriso",
        },
        "preserved": [
            "Microsoft Store",
            "Windows Update",
            "Microsoft Defender",
            "SmartScreen",
            "Microsoft Edge/WebView2",
            "Windows Terminal",
            "Windows Recovery",
        ],
    }


def _iso_has_path(iso: Path, iso_path: str) -> bool:
    import subprocess

    proc = subprocess.run(
        ["xorriso", "-indev", str(iso), "-ls", iso_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode == 0


def validate_output_iso(iso: Path) -> None:
    if not iso.is_file() or iso.stat().st_size < 1024 * 1024:
        raise BuilderError(f"Output ISO is missing or unexpectedly small: {iso}")
    required = (
        "/sources/boot.wim",
        "/sources/install.wim",
        "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd",
        "/sources/$OEM$/$$/Setup/Scripts/OS11vLIN.ps1",
        "/OS11vLIN-manifest.json",
    )
    missing = [item for item in required if not _iso_has_path(iso, item)]
    if missing:
        raise BuilderError("Output ISO validation failed; missing: " + ", ".join(missing))
    report = run_checked(["xorriso", "-indev", str(iso), "-report_el_torito", "plain"], capture_output=True)
    text = (report.stdout + report.stderr).decode("utf-8", errors="replace").casefold()
    if "el torito" not in text and "boot" not in text:
        raise BuilderError("Output ISO does not appear to contain boot metadata.")


def build_iso(
    inspection: IsoInspection,
    edition: Edition,
    output_iso: Path,
    profile_ids: list[str],
    *,
    force: bool = False,
) -> BuildResult:
    _validate_profiles(profile_ids)
    output_iso = output_iso.expanduser().resolve()
    output_iso.parent.mkdir(parents=True, exist_ok=True)
    if output_iso.exists() and not force:
        raise BuilderError(f"Output already exists: {output_iso}. Use --force to replace it.")
    if output_iso == inspection.source:
        raise BuilderError("Refusing to overwrite the source ISO.")

    current_source_hash = sha256_file(inspection.source)
    if current_source_hash != inspection.source_sha256:
        raise BuilderError("Source ISO changed after inspection; aborting build.")

    with tempfile.TemporaryDirectory(prefix="os11vlin-build-") as temporary:
        root = Path(temporary)
        selected_wim = export_selected_edition(inspection, edition, root / "install.wim")
        setup_complete, powershell = write_provisioning_files(root, profile_ids)
        manifest_data = _manifest(inspection, edition, profile_ids)
        manifest = root / "OS11vLIN-manifest.json"
        manifest.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        partial = output_iso.with_name(output_iso.name + ".building")
        partial.unlink(missing_ok=True)
        maps = [
            (selected_wim, "/sources/install.wim"),
            (setup_complete, "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd"),
            (powershell, "/sources/$OEM$/$$/Setup/Scripts/OS11vLIN.ps1"),
            (manifest, "/OS11vLIN-manifest.json"),
            (manifest, "/sources/$OEM$/$1/OS11vLIN/manifest.json"),
        ]

        command = [
            "xorriso",
            "-indev", str(inspection.source),
            "-outdev", str(partial),
            "-overwrite", "on",
        ]
        if inspection.install_format == "esd":
            command += ["-rm", "/sources/install.esd"]
        for local, target in maps:
            command += ["-map", str(local), target]
        command += ["-boot_image", "any", "replay", "-commit", "-end"]

        try:
            run_checked(command)
            validate_output_iso(partial)
            if sha256_file(inspection.source) != inspection.source_sha256:
                raise BuilderError("Source ISO was unexpectedly modified during the build.")
            if output_iso.exists():
                output_iso.unlink()
            shutil.move(str(partial), str(output_iso))
        finally:
            partial.unlink(missing_ok=True)

    output_hash = sha256_file(output_iso)
    checksum = output_iso.with_name(output_iso.name + ".sha256")
    checksum.write_text(f"{output_hash}  {output_iso.name}\n", encoding="ascii")
    return BuildResult(
        output_iso=output_iso,
        checksum_file=checksum,
        output_sha256=output_hash,
        source_sha256=inspection.source_sha256,
        edition=edition,
        profiles=tuple(profile_ids),
    )


def inspect_source(source: Path) -> tuple[IsoInspection, tempfile.TemporaryDirectory]:
    temp = tempfile.TemporaryDirectory(prefix="os11vlin-inspect-")
    try:
        inspection = inspect_iso(source, Path(temp.name))
        return inspection, temp
    except Exception:
        temp.cleanup()
        raise
