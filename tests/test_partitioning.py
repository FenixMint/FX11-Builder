import pytest

from fx11.iso import BuilderError
from fx11.partitioning import (
    ESP_MIB,
    MSR_MIB,
    ChangeKind,
    LayoutMode,
    PartitionChange,
    PartitionSpec,
    custom_diskpart_script,
    custom_plan,
    diskpart_script,
    plan_fx11_only,
    plan_other_os,
    recovery_size_mib,
    validate_plan,
)


def test_recovery_size_uses_one_gib_floor():
    assert recovery_size_mib(600 * 1024 * 1024) == 1024


def test_fx11_only_consumes_remaining_space():
    plan = plan_fx11_only(256 * 1024, 1024)
    assert plan.mode == LayoutMode.FX11_ONLY
    assert plan.allocated_mib == plan.disk_size_mib
    assert plan.unallocated_mib == 0
    assert plan.partitions[0].size_mib == ESP_MIB
    assert plan.partitions[1].size_mib == MSR_MIB
    assert plan.partitions[-1].kind == "recovery"


def test_other_os_leaves_tail_unallocated_after_recovery():
    plan = plan_other_os(1024 * 1024, 350 * 1024, 1024)
    assert plan.mode == LayoutMode.OTHER_OS
    assert plan.partitions[-2].kind == "recovery"
    assert plan.partitions[-1].kind == "other-os"
    assert plan.partitions[-1].unallocated is True
    assert plan.allocated_mib + plan.unallocated_mib == plan.disk_size_mib


def test_other_os_rejects_too_small_fx11_partition():
    with pytest.raises(BuilderError):
        plan_other_os(256 * 1024, 32 * 1024, 1024)


def test_guided_diskpart_does_not_accept_custom_plan():
    with pytest.raises(BuilderError):
        diskpart_script(custom_plan(512 * 1024), 0)


def test_disk_number_must_be_explicit_and_valid():
    plan = plan_fx11_only(256 * 1024, 1024)
    with pytest.raises(BuilderError):
        diskpart_script(plan, -1)


def test_other_os_diskpart_does_not_format_reserved_space():
    plan = plan_other_os(512 * 1024, 200 * 1024, 1024)
    script = diskpart_script(plan, 2)
    assert "select disk 2" in script
    assert 'label="FX11"' in script
    assert 'label="Recovery"' in script
    assert "Other OS" not in script
    assert "ext4" not in script
    assert "btrfs" not in script.lower()


def test_custom_layout_requires_windows_and_esp_when_defined():
    with pytest.raises(BuilderError):
        custom_plan(
            512 * 1024,
            partitions=(PartitionSpec("FX11", "windows", 200 * 1024, "NTFS"),),
        )


def test_custom_layout_accepts_preserved_other_os_and_reports_missing_recovery_warning():
    plan = custom_plan(
        512 * 1024,
        partitions=(
            PartitionSpec("Existing EFI", "esp", 300, "FAT32", partition_number=1, existing=True, preserve=True),
            PartitionSpec("MSR", "msr", 16, partition_number=2, existing=True, preserve=True),
            PartitionSpec("FX11", "windows", 200 * 1024, "NTFS", partition_number=3),
            PartitionSpec("Linux", "other-os", 200 * 1024, "ext4", partition_number=4, existing=True, preserve=True),
        ),
    )
    validation = validate_plan(plan)
    assert validation.valid is True
    assert any("Recovery" in warning for warning in validation.warnings)


def test_custom_diskpart_stages_delete_format_create_without_clean():
    plan = custom_plan(
        512 * 1024,
        partitions=(
            PartitionSpec("EFI", "esp", 300, "FAT32", partition_number=1, existing=True, preserve=True),
            PartitionSpec("MSR", "msr", 16, partition_number=2, existing=True, preserve=True),
            PartitionSpec("FX11", "windows", 200 * 1024, "NTFS"),
            PartitionSpec("Recovery", "recovery", 1024, "NTFS"),
        ),
        changes=(
            PartitionChange(ChangeKind.DELETE, partition_number=3),
            PartitionChange(ChangeKind.CREATE, size_mib=200 * 1024, filesystem="NTFS", label="FX11", kind="windows"),
            PartitionChange(ChangeKind.CREATE, size_mib=1024, filesystem="NTFS", label="Recovery", kind="recovery"),
        ),
    )
    script = custom_diskpart_script(plan, 0)
    assert "select disk 0" in script
    assert "delete partition override" in script
    assert 'label="FX11"' in script
    assert "de94bba4-06d1-4d40-a16a-bfd50179d6ac" in script
    assert "clean" not in script.lower()


def test_custom_resize_refuses_ambiguous_diskpart_generation():
    plan = custom_plan(
        512 * 1024,
        partitions=(
            PartitionSpec("EFI", "esp", 300, "FAT32", partition_number=1, existing=True, preserve=True),
            PartitionSpec("MSR", "msr", 16, partition_number=2, existing=True, preserve=True),
            PartitionSpec("FX11", "windows", 200 * 1024, "NTFS", partition_number=3, existing=True),
            PartitionSpec("Recovery", "recovery", 1024, "NTFS", partition_number=4, existing=True),
        ),
        changes=(PartitionChange(ChangeKind.RESIZE, partition_number=3, size_mib=180 * 1024),),
    )
    with pytest.raises(BuilderError):
        custom_diskpart_script(plan, 0)
