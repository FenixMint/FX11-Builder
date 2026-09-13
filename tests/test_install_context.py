from pathlib import Path

import pytest

from fx11.install_context import InstallContext, PartitionRef, read_install_context, write_install_context
from fx11.iso import BuilderError
from fx11.partitioning import LayoutMode


def test_install_context_roundtrip(tmp_path: Path):
    context = InstallContext(
        layout_mode=LayoutMode.OTHER_OS,
        disk_number=0,
        disk_model="Test NVMe 1TB",
        disk_size_mib=1024 * 1024,
        windows=PartitionRef(0, 3, volume_id="VOL-FX11", label="FX11"),
        esp=PartitionRef(0, 1, volume_id="VOL-ESP", label="System"),
        recovery=PartitionRef(0, 4, volume_id="VOL-REC", label="Recovery"),
        preserved=(PartitionRef(0, 5, volume_id="VOL-LINUX", label="Linux"),),
        other_os_unallocated_mib=400 * 1024,
        acknowledged_warnings=("Existing operating system preserved",),
    )
    path = write_install_context(context, tmp_path / "install-context.json")
    loaded = read_install_context(path)
    assert loaded == context


def test_install_context_rejects_esp_on_another_disk(tmp_path: Path):
    context = InstallContext(
        layout_mode=LayoutMode.CUSTOM,
        disk_number=0,
        disk_model="Disk 0",
        disk_size_mib=512 * 1024,
        windows=PartitionRef(0, 3),
        esp=PartitionRef(1, 1),
    )
    with pytest.raises(BuilderError):
        write_install_context(context, tmp_path / "bad.json")
