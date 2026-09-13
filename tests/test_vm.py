from pathlib import Path

from fx11 import vm


def test_qemu_baseline_avoids_virtio_driver_dependency(monkeypatch):
    monkeypatch.setattr(vm.shutil, "which", lambda name: "/usr/bin/qemu-system-x86_64")

    command = vm.qemu_command(
        Path("/tmp/fx11.iso"),
        Path("/tmp/fx11-test.raw"),
        memory_mb=4096,
        cpus=2,
        uefi=False,
    )
    joined = " ".join(command)

    assert "file=/tmp/fx11-test.raw,format=raw,if=ide" in command
    assert "e1000,netdev=n0" in command
    assert "-vga" in command
    assert "std" in command
    assert "virtio" not in joined.casefold()
    assert "FX11-test" in command
