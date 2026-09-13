from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

from .iso import BuilderError


MIB = 1024 * 1024
GIB = 1024 * MIB

# Microsoft currently requires at least 200 MiB ESP on 512/512e media and
# 300 MiB on 4Kn media. FX11 uses 300 MiB for its automatic layout so one
# layout is safe for both sector models.
ESP_MIB = 300
MSR_MIB = 16

# Microsoft recommends enough room for winre.wim + customizations + 250 MiB
# free space and documents 990 MiB as a recommended minimum for custom
# deployment layouts. FX11 rounds that safety floor up to 1024 MiB.
RECOVERY_MIN_MIB = 1024
RECOVERY_FREE_MIB = 250

# Product policy, not a Microsoft minimum. Automatic mode should not produce
# an impractically small Windows installation.
FX11_MIN_WINDOWS_GIB = 64
OTHER_OS_MIN_GIB = 16


class LayoutMode(str, Enum):
    FX11_ONLY = "fx11-only"
    OTHER_OS = "other-os"
    CUSTOM = "custom"


@dataclass(frozen=True)
class PartitionSpec:
    name: str
    kind: str
    size_mib: int | None
    filesystem: str | None = None
    unallocated: bool = False


@dataclass(frozen=True)
class PartitionPlan:
    mode: LayoutMode
    disk_size_mib: int
    partitions: tuple[PartitionSpec, ...]

    @property
    def allocated_mib(self) -> int:
        return sum(part.size_mib or 0 for part in self.partitions if not part.unallocated)

    @property
    def unallocated_mib(self) -> int:
        return sum(part.size_mib or 0 for part in self.partitions if part.unallocated)


def recovery_size_mib(winre_size_bytes: int, customizations_bytes: int = 0) -> int:
    if winre_size_bytes < 0 or customizations_bytes < 0:
        raise BuilderError("Recovery image sizes cannot be negative.")
    required = math.ceil((winre_size_bytes + customizations_bytes) / MIB) + RECOVERY_FREE_MIB
    return max(RECOVERY_MIN_MIB, required)


def _base_overhead_mib(recovery_mib: int) -> int:
    return ESP_MIB + MSR_MIB + recovery_mib


def plan_fx11_only(disk_size_mib: int, recovery_mib: int) -> PartitionPlan:
    overhead = _base_overhead_mib(recovery_mib)
    windows_mib = disk_size_mib - overhead
    if windows_mib < FX11_MIN_WINDOWS_GIB * 1024:
        raise BuilderError("Selected disk is too small for the automatic FX11 layout.")
    return PartitionPlan(
        mode=LayoutMode.FX11_ONLY,
        disk_size_mib=disk_size_mib,
        partitions=(
            PartitionSpec("EFI System", "esp", ESP_MIB, "FAT32"),
            PartitionSpec("Microsoft Reserved", "msr", MSR_MIB),
            PartitionSpec("FX11 / Windows", "windows", windows_mib, "NTFS"),
            PartitionSpec("Windows Recovery", "recovery", recovery_mib, "NTFS"),
        ),
    )


def plan_other_os(disk_size_mib: int, fx11_size_mib: int, recovery_mib: int) -> PartitionPlan:
    if fx11_size_mib < FX11_MIN_WINDOWS_GIB * 1024:
        raise BuilderError(f"FX11 partition must be at least {FX11_MIN_WINDOWS_GIB} GiB in automatic mode.")
    overhead = _base_overhead_mib(recovery_mib)
    other_mib = disk_size_mib - overhead - fx11_size_mib
    if other_mib < OTHER_OS_MIN_GIB * 1024:
        raise BuilderError(f"Other OS reserved space must be at least {OTHER_OS_MIN_GIB} GiB in automatic mode.")
    return PartitionPlan(
        mode=LayoutMode.OTHER_OS,
        disk_size_mib=disk_size_mib,
        partitions=(
            PartitionSpec("EFI System", "esp", ESP_MIB, "FAT32"),
            PartitionSpec("Microsoft Reserved", "msr", MSR_MIB),
            PartitionSpec("FX11 / Windows", "windows", fx11_size_mib, "NTFS"),
            PartitionSpec("Windows Recovery", "recovery", recovery_mib, "NTFS"),
            PartitionSpec("Other OS", "other-os", other_mib, None, unallocated=True),
        ),
    )


def custom_plan(disk_size_mib: int) -> PartitionPlan:
    if disk_size_mib <= 0:
        raise BuilderError("Disk size must be positive.")
    return PartitionPlan(LayoutMode.CUSTOM, disk_size_mib, tuple())


def diskpart_script(plan: PartitionPlan, disk_number: int) -> str:
    if plan.mode == LayoutMode.CUSTOM:
        raise BuilderError("Custom layout must not generate a destructive DiskPart script.")
    if disk_number < 0:
        raise BuilderError("Disk number must be selected explicitly.")

    windows = next(part for part in plan.partitions if part.kind == "windows")
    recovery = next(part for part in plan.partitions if part.kind == "recovery")
    lines = [
        f"select disk {disk_number}",
        "clean",
        "convert gpt",
        f"create partition efi size={ESP_MIB}",
        'format quick fs=fat32 label="System"',
        "assign letter=S",
        f"create partition msr size={MSR_MIB}",
        f"create partition primary size={windows.size_mib}",
        'format quick fs=ntfs label="FX11"',
        "assign letter=W",
        f"create partition primary size={recovery.size_mib}",
        'format quick fs=ntfs label="Recovery"',
        "assign letter=R",
        "set id=de94bba4-06d1-4d40-a16a-bfd50179d6ac",
        "gpt attributes=0x8000000000000001",
    ]
    # In Other OS mode we intentionally stop here. The remainder of the disk
    # stays unallocated; no Linux/BSD/Unix filesystem is guessed or created.
    return "\r\n".join(lines) + "\r\n"
