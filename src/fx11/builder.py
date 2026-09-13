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
from .gparted import VerifiedGPartedLive, verify_gparted_live
from .iso import BuilderError, Edition, IsoInspection, inspect_iso, run_checked, sha256_file
from .media_boot import build_media_grub_config
from .profiles import get_profile, validate_profile
from .provisioning import write_provisioning_files
from .winpe import CustomizedBootWim, customize_boot_wim


@dataclass(frozen=True)
class BuildResult:
    output_iso: Path
    checksum_file: Path
    output_sha256: str
    source_sha256: str
    edition: Edition
    profiles: tuple[str, ...]
    gparted_live: str | None = None


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
    winpe: CustomizedBootWim,
    gparted: VerifiedGPartedLive | None,
    media_grub_sha256: str | None,
) -> dict[str, object]:
    manifest: dict[str, object] = {
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
        "winpe": {
            "boot_wim_image_index": winpe.image_index,
            "source_boot_wim_sha256": winpe.source_sha256,
            "fx11_boot_wim_sha256": winpe.output_sha256,
            "startup": "winpeshl.ini -> cmd.exe /c Startnet.cmd -> wpeinit -> X:\\FX11\\fx11-launch.cmd",
            "current_frontend": "text-mode FX Partition Manager with guided layouts, manual Custom path and direct FX11 deployment handoff",
            "direct_deployment": "DISM /Apply-Image -> stage FX11 provisioning -> BCDBoot -> optional WinRE",
            "stock_setup_fallback": True,
        },
        "partition_manager": {
            "mainline_direction": "FX-branded graphical environment powered by GParted",
            "text_fallback_retained": True,
            "gparted_payload_staged": gparted is not None,
            "gparted_media_grub_staged": media_grub_sha256 is not None,
            "gparted_boot_selector_status": "media GRUB config staged; UEFI El Torito handoff to FX GRUB still pending",
        },
        "boot_manager": {
            "name": "FX Boot Manager",
            "implementation": "GRUB x86_64 UEFI standalone development payload",
            "secure_boot_compatible": False,
            "secure_boot_policy": "Current development payload requires Secure Boot to be disabled; firmware settings are never changed automatically.",
            "installation_role": "FX11 Installer stages the development payload on the selected ESP after BCDBoot; automatic firmware-default activation is still pending.",
        },
        "strategy": {
            "edition": "selected image exported with wimlib to a single-image install.wim",
            "deployment": "FX11 WinPE applies install.wim index 1 directly to the partition prepared by FX Partition Manager",
            "debloat": "FX11 provisioning scripts are staged into Windows Setup Scripts after image application; real-hardware/OOBE execution still requires validation",
            "privacy": "machine/default-user policy is applied by the staged FX11 provisioning script",
            "iso_boot": "original ISO boot metadata replayed by xorriso; boot.wim boot image is customized to start FX11 first",
            "installed_boot": "BCDBoot creates reliable Windows UEFI boot files; FX Boot Manager files are staged on the ESP for later firmware-default activation",
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

    if gparted is not None:
        gparted_iso_path = f"/FX11/gparted/{gparted.spec.filename}"
        manifest["third_party"] = {
            "gparted_live": {
                "version": gparted.spec.version,
                "gparted_version": gparted.spec.gparted_version,
                "architecture": gparted.spec.architecture,
                "kernel": gparted.spec.kernel,
                "filename": gparted.spec.filename,
                "iso_path": gparted_iso_path,
                "sha256": gparted.sha256,
                "upstream_release_page": gparted.spec.release_page,
                "project_home": gparted.spec.project_home,
                "branding_policy": "FX Partition Manager — powered by GParted; upstream identity and license obligations are retained.",
            }
        }
        if media_grub_sha256 is not None:
            injected = manifest.get("injected_files")
            if isinstance(injected, dict):
                injected["/FX11/media/grub.cfg"] = {
                    "sha256": media_grub_sha256,
                    "purpose": "Top-level FX installation-media GRUB menu for GParted mainline and WinPE fallback",
                }

    return manifest


def _iso_has_path(iso: Path, iso_path: str) -> bool:
    proc = subprocess.run(
        ["xorriso", "-indev", str(iso), "-ls", iso_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode == 0


def validate_output_iso(iso: Path, *, extra_required: tuple[str, ...] = tuple()) -> None:
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
        *extra_required,
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
    gparted_live: Path | None = None,
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

    verified_gparted = verify_gparted_live(gparted_live) if gparted_live is not None else None
    gparted_iso_path = (
        f"/FX11/gparted/{verified_gparted.spec.filename}" if verified_gparted is not None else None
    )

    with tempfile.TemporaryDirectory(prefix="fx11-build-") as temporary:
        root = Path(temporary)
        selected_wim = export_selected_edition(inspection, edition, root / "install.wim")
        customized_boot = customize_boot_wim(inspection.source, root / "winpe")
        setup_complete, powershell, injected_hashes = write_provisioning_files(root, profile_ids)
        boot_payload = build_unsigned_payload(root / "fxboot")
        boot_hashes = {
            "fxbootx64.efi": sha256_file(boot_payload.efi_binary),
            "grub.cfg": sha256_file(boot_payload.grub_config),
            "theme.txt": sha256_file(boot_payload.theme_config),
        }

        media_grub: Path | None = None
        media_grub_sha256: str | None = None
        if verified_gparted is not None:
            media_boot = build_media_grub_config()
            media_grub = root / "media-grub.cfg"
            media_grub.write_text(media_boot.grub_config, encoding="utf-8")
            media_grub_sha256 = sha256_file(media_grub)

        manifest_data = _manifest(
            inspection,
            edition,
            profile_ids,
            injected_hashes,
            boot_hashes,
            customized_boot,
            verified_gparted,
            media_grub_sha256,
        )
        manifest = root / "FX11-manifest.json"
        manifest.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        partial = output_iso.with_name(output_iso.name + ".building")
        partial.unlink(missing_ok=True)
        maps: list[tuple[Path, str]] = [
            (customized_boot.path, "/sources/boot.wim"),
            (selected_wim, "/sources/install.wim"),
            (setup_complete, "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd"),
            (powershell, "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1"),
            (manifest, "/FX11-manifest.json"),
            (manifest, "/sources/$OEM$/$1/FX11/manifest.json"),
            (boot_payload.efi_binary, "/FX11/boot/EFI/FX11/fxbootx64.efi"),
            (boot_payload.grub_config, "/FX11/boot/EFI/FX11/grub.cfg"),
            (boot_payload.theme_config, "/FX11/boot/EFI/FX11/theme/theme.txt"),
        ]
        required_extra_list: list[str] = []
        if verified_gparted is not None and gparted_iso_path is not None:
            maps.append((verified_gparted.path, gparted_iso_path))
            required_extra_list.append(gparted_iso_path)
        if media_grub is not None:
            maps.append((media_grub, "/FX11/media/grub.cfg"))
            required_extra_list.append("/FX11/media/grub.cfg")

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
            validate_output_iso(partial, extra_required=tuple(required_extra_list))
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
        gparted_live=verified_gparted.spec.version if verified_gparted is not None else None,
    )


def inspect_source(source: Path) -> tuple[IsoInspection, tempfile.TemporaryDirectory]:
    temp = tempfile.TemporaryDirectory(prefix="fx11-inspect-")
    try:
        inspection = inspect_iso(source, Path(temp.name))
        return inspection, temp
    except Exception:
        temp.cleanup()
        raise
