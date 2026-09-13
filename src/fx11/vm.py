from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
import tempfile

from .iso import BuilderError


OVMF_CANDIDATES = (
    Path("/usr/share/OVMF/OVMF_CODE.fd"),
    Path("/usr/share/OVMF/OVMF_CODE_4M.fd"),
    Path("/usr/share/edk2/ovmf/OVMF_CODE.fd"),
    Path("/usr/share/edk2/x64/OVMF_CODE.fd"),
)


def find_ovmf() -> Path | None:
    for candidate in OVMF_CANDIDATES:
        if candidate.is_file():
            return candidate
    return None


def qemu_command(iso: Path, disk: Path, *, memory_mb: int = 4096, cpus: int = 2, uefi: bool = True) -> list[str]:
    if shutil.which("qemu-system-x86_64") is None:
        raise BuilderError("qemu-system-x86_64 is not installed.")

    # Baseline VM hardware intentionally uses devices with inbox Windows/WinPE
    # support.  Requiring virtio storage/network drivers here would make the
    # installer test depend on a second driver ISO and could hide FX11 issues
    # behind a missing third-party driver.
    command = [
        "qemu-system-x86_64",
        "-name", "FX11-test",
        "-m", str(memory_mb),
        "-smp", str(cpus),
        "-machine", "q35",
        "-cpu", "host" if Path("/dev/kvm").exists() else "max",
        "-cdrom", str(iso),
        "-drive", f"file={disk},format=raw,if=ide",
        "-boot", "order=d,menu=on",
        "-device", "e1000,netdev=n0",
        "-netdev", "user,id=n0",
        "-vga", "std",
    ]
    if Path("/dev/kvm").exists() and os.access("/dev/kvm", os.R_OK | os.W_OK):
        command += ["-enable-kvm"]
    if uefi:
        ovmf = find_ovmf()
        if ovmf is None:
            raise BuilderError("UEFI test requested but OVMF firmware was not found. Install ovmf or use --bios.")
        command += ["-drive", f"if=pflash,format=raw,readonly=on,file={ovmf}"]
    return command


def launch_qemu(iso: Path, *, memory_mb: int = 4096, cpus: int = 2, disk_gb: int = 64, uefi: bool = True) -> int:
    iso = iso.expanduser().resolve()
    if not iso.is_file():
        raise BuilderError(f"ISO not found: {iso}")
    with tempfile.TemporaryDirectory(prefix="fx11-qemu-") as temporary:
        disk = Path(temporary) / "windows-test.raw"
        with disk.open("wb") as handle:
            handle.truncate(disk_gb * 1024 * 1024 * 1024)
        command = qemu_command(iso, disk, memory_mb=memory_mb, cpus=cpus, uefi=uefi)
        return subprocess.call(command)
