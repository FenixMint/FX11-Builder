from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from . import __version__
from .bootmanager import build_unsigned_payload
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


def _tool_record(command: str, version_args: list[str]) -> dict[str, str]:
    path = shutil.which(command) or ""
    version = "unknown"
    if path:
        try:
            proc = subprocess.run(
                [path, *version_args],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=10,
            )
            text = proc.stdout.decode("utf-8", errors="replace").strip()
            if text:
                version = text.splitlines()[0].strip()
        except (OSError, subprocess.SubprocessError):
            pass
    return {"path": path, "version": version}


def _build_tools() -> dict[str, object]:
    return {
        "python": {"path": sys.executable, "version": sys.version.split()[0]},
        "wimlib-imagex": _tool_record("wimlib-imagex", ["--version"]),
        "xorriso": _tool_record("xorriso", ["-version"]),
        "grub-mkstandalone": _tool_record("grub-mkstandalone", ["--version"]),
    }


def _manifest(
    inspection: IsoInspection,
    edition: Edition,
    profile_ids: list[str],
    injected_hashes: dict[str, str],
    boot_hashes: dict[str, str],
) -> dict[str, object]:
    return {
        "project": "FX11 Builder",
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
        "build_tools": _build_tools(),
        "injected_files": {
            "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd": {
                "sha256": injected_hashes["SetupComplete.cmd"],
                "purpose": "Verify and launch FX11 provisioning",
            },
            "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1": {
                "sha256": injected_hashes["FX11.ps1"],
                "purpose": "Declared FX11 provisioning actions",
            },
            "/FX11/boot/EFI/FX11/fxbootx64.efi": {
                "sha256": boot_hashes["fxbootx64.efi"],
                "purpose": "Unsigned development FX Boot Manager UEFI binary",
            },
            "/FX11/boot/EFI/FX11/grub.cfg": {
                "sha256": boot_hashes["grub.cfg"],
                "purpose": "FX Boot Manager GRUB configuration template",
            },
            "/FX11/boot/EFI/FX11/theme/theme.txt": {
                "sha256": boot_hashes["theme.txt"],
                "purpose": "FX Boot Manager visual theme",
            },
        },
        "boot_manager": {
            "name": "FX Boot Manager",
            "implementation": "GRUB x86_64 UEFI standalone development payload",
            "secure_boot_compatible": False,
            "secure_boot_policy": "Current development payload requires Secure Boot to be disabled; firmware settings are never changed automatically.",
            "installation_role": "Installed later by FX11 Installer onto the selected ESP after Windows boot files are prepared.",
        },
        "strategy": {
            "edition": "selected image exported with wimlib to a single-image install.wim",
            "debloat": "Windows SetupComplete removes declared provisioned AppX packages using Windows servicing APIs",
            "privacy": "machine/default-user policy applied during SetupComplete",
            "iso_boot": "original ISO boot metadata replayed by xorriso",
            "installed_boot": "FX Boot Manager development payload is embedded for later ESP installation; FX11 chainloads Windows Boot Manager",
            "integrity": "SetupComplete verifies the SHA-256 of FX11.ps1 before executing it",
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
        "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1",
        "/FX11-manifest.json",
        "/FX11/boot/EFI/FX11/fxbootx64.efi",
        "/FX11/boot/EFI/FX11/grub.cfg",
        "/FX11/boot/EFI/FX11/theme/theme.txt",
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

    with tempfile.TemporaryDirectory(prefix="fx11-build-") as temporary:
        root = Path(temporary)
        selected_wim = export_selected_edition(inspection, edition, root / "install.wim")
        setup_complete, powershell, injected_hashes = write_provisioning_files(root, profile_ids)
        boot_payload = build_unsigned_payload(root / "fxboot")
        boot_hashes = {
            "fxbootx64.efi": sha256_file(boot_payload.efi_binary),
            "grub.cfg": sha256_file(boot_payload.grub_config),
            "theme.txt": sha256_file(boot_payload.theme_config),
        }
        manifest_data = _manifest(inspection, edition, profile_ids, injected_hashes, boot_hashes)
        manifest = root / "FX11-manifest.json"
        manifest.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        partial = output_iso.with_name(output_iso.name + ".building")
        partial.unlink(missing_ok=True)
        maps = [
            (selected_wim, "/sources/install.wim"),
            (setup_complete, "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd"),
            (powershell, "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1"),
            (manifest, "/FX11-manifest.json"),
            (manifest, "/sources/$OEM$/$1/FX11/manifest.json"),
            (boot_payload.efi_binary, "/FX11/boot/EFI/FX11/fxbootx64.efi"),
            (boot_payload.grub_config, "/FX11/boot/EFI/FX11/grub.cfg"),
            (boot_payload.theme_config, "/FX11/boot/EFI/FX11/theme/theme.txt"),
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
    temp = tempfile.TemporaryDirectory(prefix="fx11-inspect-")
    try:
        inspection = inspect_iso(source, Path(temp.name))
        return inspection, temp
    except Exception:
        temp.cleanup()
        raise
