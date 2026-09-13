import pytest

from fx11.iso import BuilderError
from fx11.partitioning import (
    ESP_MIB,
    MSR_MIB,
    LayoutMode,
    custom_plan,
    diskpart_script,
    plan_fx11_only,
    plan_other_os,
    recovery_size_mib,
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


def test_custom_never_generates_destructive_diskpart():
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
