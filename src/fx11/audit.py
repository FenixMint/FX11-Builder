from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from .iso import (
    BuilderError,
    detect_media_format,
    extract_install_image,
    extract_iso_member,
    read_editions,
    sha256_file,
)


@dataclass(frozen=True)
class IsoDelta:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    common_count: int


@dataclass(frozen=True)
class WimDelta:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    common_count: int


def _normalize_path(value: str) -> str:
    value = value.strip().strip("'").strip('"')
    if not value.startswith("/"):
        value = "/" + value
    return value.replace("\\", "/")


def _run(args: list[str], label: str) -> subprocess.CompletedProcess:
    proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"{label}: {detail}")
    return proc


def parse_7z_slt_files(text: str) -> tuple[str, ...]:
    """Parse file paths from `7z l -slt` output, ignoring directories and archive metadata."""
    files: set[str] = set()
    record: dict[str, str] = {}

    def flush() -> None:
        if not record:
            return
        path = record.get("Path", "").strip()
        if not path or "Type" in record:
            return
        folder = record.get("Folder", "").strip().casefold()
        attrs = record.get("Attributes", "").strip().upper()
        if folder in {"+", "1", "true"} or attrs.startswith("D"):
            return
        files.add(_normalize_path(path))

    for raw in text.splitlines():
        line = raw.rstrip("\r\n")
        if not line.strip():
            flush()
            record = {}
            continue
        if " = " not in line:
            continue
        key, value = line.split(" = ", 1)
        record[key.strip()] = value.strip()
    flush()
    return tuple(sorted(files))


def list_iso_files(iso: Path) -> tuple[str, ...]:
    iso = iso.expanduser().resolve()
    if not iso.is_file():
        raise BuilderError(f"ISO not found: {iso}")

    if detect_media_format(iso) == "udf":
        sevenzip = shutil.which("7z")
        if sevenzip is None:
            raise BuilderError("7z is required to inventory UDF Microsoft installation media.")
        proc = _run([sevenzip, "l", "-slt", str(iso)], "Unable to inventory UDF ISO with 7-Zip")
        files = parse_7z_slt_files(proc.stdout.decode("utf-8", errors="replace"))
        if not files:
            raise BuilderError("7-Zip returned no file inventory for the UDF ISO.")
        return files

    proc = _run(
        ["xorriso", "-indev", str(iso), "-find", "/", "-type", "f", "-exec", "lsdl", "--"],
        "Unable to inventory ISO with xorriso",
    )

    files: set[str] = set()
    text = proc.stdout.decode("utf-8", errors="replace")
    for line in text.splitlines():
        match = re.search(r"['\"](/[^'\"]*)['\"]\s*$", line)
        if match:
            files.add(_normalize_path(match.group(1)))
            continue
        stripped = line.strip()
        if stripped.startswith("/"):
            files.add(_normalize_path(stripped))
    if not files:
        raise BuilderError("xorriso returned no file inventory for the ISO.")
    return tuple(sorted(files))


def compare_inventories(source_files: tuple[str, ...], output_files: tuple[str, ...]) -> IsoDelta:
    source = set(source_files)
    output = set(output_files)
    return IsoDelta(
        added=tuple(sorted(output - source)),
        removed=tuple(sorted(source - output)),
        common_count=len(source & output),
    )


def extract_iso_path(iso: Path, iso_path: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    return extract_iso_member(iso, iso_path, destination)


def _read_fx11_manifest(output_iso: Path, work: Path) -> dict[str, object]:
    target = extract_iso_path(output_iso, "/FX11-manifest.json", work / "FX11-manifest.json")
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise BuilderError(f"Unable to parse FX11 manifest: {exc}") from exc


def _expected_fx11_paths(manifest: dict[str, object]) -> set[str]:
    expected = {
        "/FX11-manifest.json",
        "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd",
        "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1",
        "/sources/$OEM$/$1/FX11/manifest.json",
        "/FX11/boot/EFI/FX11/fxbootx64.efi",
        "/FX11/boot/EFI/FX11/grub.cfg",
        "/FX11/boot/EFI/FX11/theme/theme.txt",
    }

    injected = manifest.get("injected_files")
    if isinstance(injected, dict):
        for path in injected:
            if isinstance(path, str) and path.startswith("/"):
                expected.add(path)

    third_party = manifest.get("third_party")
    if isinstance(third_party, dict):
        gparted = third_party.get("gparted_live")
        if isinstance(gparted, dict):
            iso_path = gparted.get("iso_path")
            if isinstance(iso_path, str) and iso_path.startswith("/"):
                expected.add(iso_path)

    return expected


def list_wim_files(wim: Path, index: int) -> tuple[str, ...]:
    proc = _run(
        ["wimlib-imagex", "dir", str(wim), str(index), "/"],
        f"Unable to inventory WIM image {index}",
    )
    files: set[str] = set()
    for raw in proc.stdout.decode("utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("Available") or line.startswith("Directory of"):
            continue
        candidate = line.split()[-1].strip('"')
        if candidate.startswith(("/", "\\")):
            files.add(_normalize_path(candidate))
    if not files:
        raise BuilderError("wimlib-imagex returned no file inventory for the selected Windows image.")
    return tuple(sorted(files))


def compare_wim_inventories(source_files: tuple[str, ...], output_files: tuple[str, ...]) -> WimDelta:
    source = set(source_files)
    output = set(output_files)
    return WimDelta(
        added=tuple(sorted(output - source)),
        removed=tuple(sorted(source - output)),
        common_count=len(source & output),
    )


def _wim_metadata(wim: Path) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for edition in read_editions(wim):
        result.append(
            {
                "index": edition.index,
                "name": edition.name,
                "edition_id": edition.edition_id,
                "architecture": edition.architecture,
                "description": edition.description,
            }
        )
    return result


def build_delta_report(source_iso: Path, output_iso: Path) -> dict[str, object]:
    source_iso = source_iso.expanduser().resolve()
    output_iso = output_iso.expanduser().resolve()
    source_files = list_iso_files(source_iso)
    output_files = list_iso_files(output_iso)
    delta = compare_inventories(source_files, output_files)

    with tempfile.TemporaryDirectory(prefix="fx11-audit-") as temp_name:
        work = Path(temp_name)
        manifest = _read_fx11_manifest(output_iso, work)
        expected_fx11_paths = _expected_fx11_paths(manifest)
        unexpected_added = tuple(sorted(path for path in delta.added if path not in expected_fx11_paths))

        source_index_raw = manifest.get("edition", {}).get("source_index", 0) if isinstance(manifest.get("edition"), dict) else 0
        try:
            source_index = int(source_index_raw)
        except (TypeError, ValueError) as exc:
            raise BuilderError("FX11 manifest does not contain a valid source edition index.") from exc

        source_wim, source_format = extract_install_image(source_iso, work / "source")
        output_wim, output_format = extract_install_image(output_iso, work / "output")
        output_editions = read_editions(output_wim)
        if len(output_editions) != 1:
            raise BuilderError("FX11 output install image should contain exactly one Windows edition.")
        output_index = output_editions[0].index

        source_wim_files = list_wim_files(source_wim, source_index)
        output_wim_files = list_wim_files(output_wim, output_index)
        wim_delta = compare_wim_inventories(source_wim_files, output_wim_files)

        injected_hashes: dict[str, str] = {}
        for iso_path in sorted(expected_fx11_paths):
            if iso_path not in output_files:
                continue
            extracted = extract_iso_path(output_iso, iso_path, work / "injected" / iso_path.lstrip("/").replace("/", "__"))
            injected_hashes[iso_path] = sha256_file(extracted)

        return {
            "schema": "fx11-iso-delta-v2",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "source": {
                "path": str(source_iso),
                "sha256": sha256_file(source_iso),
                "file_count": len(source_files),
                "install_format": source_format,
                "install_images": _wim_metadata(source_wim),
                "audited_image_index": source_index,
            },
            "output": {
                "path": str(output_iso),
                "sha256": sha256_file(output_iso),
                "file_count": len(output_files),
                "install_format": output_format,
                "install_images": _wim_metadata(output_wim),
                "audited_image_index": output_index,
            },
            "iso_delta": {
                "added": list(delta.added),
                "removed": list(delta.removed),
                "common_count": delta.common_count,
                "unexpected_added": list(unexpected_added),
            },
            "install_image_delta": {
                "source_file_count": len(source_wim_files),
                "output_file_count": len(output_wim_files),
                "added": list(wim_delta.added),
                "removed": list(wim_delta.removed),
                "common_count": wim_delta.common_count,
                "content_inventory_identical": not wim_delta.added and not wim_delta.removed,
            },
            "fx11_manifest": manifest,
            "injected_file_sha256": injected_hashes,
            "expected_fx11_additions": sorted(expected_fx11_paths),
            "security_interpretation": {
                "offline_install_image_changed": bool(wim_delta.added or wim_delta.removed),
                "unexpected_iso_additions": list(unexpected_added),
                "note": (
                    "FX11 currently exports the selected Windows image and performs declared AppX/privacy actions later via SetupComplete. "
                    "FX Boot Manager development files are added outside install.wim and are expected ISO-level additions. "
                    "Therefore a clean build is expected to have identical selected-image path inventory while declared FX11 files are added outside install.wim."
                ),
            },
            "runtime_audit_required": [
                "registry changes after SetupComplete",
                "services and service start modes",
                "scheduled tasks",
                "Run/RunOnce and startup entries",
                "firewall rules",
                "Defender and SmartScreen configuration",
                "certificate stores and trusted roots",
                "local users and groups",
                "installed drivers",
                "installed/provisioned AppX inventory",
                "network destinations during Setup, OOBE and FX11 First Run",
                "installed ESP contents and UEFI boot order",
            ],
            "notes": [
                "This v2 report performs ISO/UDF filesystem and selected install-image path inventory comparison.",
                "Runtime state cannot be proven from ISO contents alone; the remaining runtime checks require an installed disposable VM snapshot.",
                "The current FX Boot Manager payload is intentionally unsigned and requires Secure Boot off during development.",
                "File-path equality inside WIM does not prove byte-for-byte equality of every file; a later forensic mode can hash selected or all WIM file payloads when performance permits.",
            ],
        }


def write_delta_report(source_iso: Path, output_iso: Path, report_path: Path) -> dict[str, object]:
    report = build_delta_report(source_iso, output_iso)
    report_path = report_path.expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
