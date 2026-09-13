from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

from .iso import BuilderError, sha256_file


@dataclass(frozen=True)
class IsoDelta:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    common_count: int


def _normalize_path(value: str) -> str:
    value = value.strip().strip("'").strip('"')
    if not value.startswith("/"):
        value = "/" + value
    return value


def list_iso_files(iso: Path) -> tuple[str, ...]:
    iso = iso.expanduser().resolve()
    if not iso.is_file():
        raise BuilderError(f"ISO not found: {iso}")
    proc = subprocess.run(
        ["xorriso", "-indev", str(iso), "-find", "/", "-type", "f", "-exec", "lsdl", "--"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to inventory ISO with xorriso: {detail}")

    files: set[str] = set()
    text = proc.stdout.decode("utf-8", errors="replace")
    for line in text.splitlines():
        # xorriso lsdl output normally ends with a quoted absolute ISO path.
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


def build_delta_report(source_iso: Path, output_iso: Path) -> dict[str, object]:
    source_iso = source_iso.expanduser().resolve()
    output_iso = output_iso.expanduser().resolve()
    source_files = list_iso_files(source_iso)
    output_files = list_iso_files(output_iso)
    delta = compare_inventories(source_files, output_files)

    expected_fx11_paths = {
        "/FX11-manifest.json",
        "/sources/$OEM$/$$/Setup/Scripts/SetupComplete.cmd",
        "/sources/$OEM$/$$/Setup/Scripts/FX11.ps1",
        "/sources/$OEM$/$1/FX11/manifest.json",
    }
    unexpected_added = tuple(sorted(path for path in delta.added if path not in expected_fx11_paths))

    return {
        "schema": "fx11-iso-delta-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": str(source_iso),
            "sha256": sha256_file(source_iso),
            "file_count": len(source_files),
        },
        "output": {
            "path": str(output_iso),
            "sha256": sha256_file(output_iso),
            "file_count": len(output_files),
        },
        "delta": {
            "added": list(delta.added),
            "removed": list(delta.removed),
            "common_count": delta.common_count,
            "unexpected_added": list(unexpected_added),
        },
        "expected_fx11_additions": sorted(expected_fx11_paths),
        "notes": [
            "This v1 report compares the ISO filesystem inventory only.",
            "A changed install.wim appears as the same ISO path and is not expanded here.",
            "Future audit stages will compare WIM contents, registry hives, services, tasks, drivers and certificates.",
        ],
    }


def write_delta_report(source_iso: Path, output_iso: Path, report_path: Path) -> dict[str, object]:
    report = build_delta_report(source_iso, output_iso)
    report_path = report_path.expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
