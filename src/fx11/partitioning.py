from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

from .iso import BuilderError


MIB = 1024 * 1024
GIB = 1024 * MIB

ESP_MIB = 300
MSR_MIB = 16
RECOVERY_MIN_MIB = 1024
RECOVERY_FREE_MIB = 250
FX11_MIN_WINDOWS_GIB = 64
OTHER_OS_MIN_GIB = 16


class LayoutMode(str, Enum):
    FX11_ONLY = "fx11-only"
    OTHER_OS = "other-os"
    CUSTOM = "custom"


class ChangeKind(str, Enum):
    CREATE = "create"
    DELETE = "delete"
    RESIZE = "resize"
    FORMAT = "format"
    PRESERVE = "preserve"


@dataclass(frozen=True)
class PartitionSpec:
    name: str
    kind: str
    size_mib: int | None
    filesystem: str | None = None
    unallocated: bool = False
    partition_number: int | None = None
    existing: bool = False
    preserve: bool = False


@dataclass(frozen=True)
class PartitionChange:
    action: ChangeKind
    partition_number: int | None = None
    size_mib: int | None = None
    filesystem: str | None = None
    label: str | None = None
    kind: str | None = None


@dataclass(frozen=True)
class PartitionPlan:
    mode: LayoutMode
    disk_size_mib: int
    partitions: tuple[PartitionSpec, ...]
    changes: tuple[PartitionChange, ...] = tuple()

    @property
    def allocated_mib(self) -> int:
        return sum(part.size_mib or 0 for part in self.partitions if not part.unallocated)

    @property
    def unallocated_mib(self) -> int:
        return sum(part.size_mib or 0 for part in self.partitions if part.unallocated)

    def first(self, kind: str) -> PartitionSpec | None:
        return next((part for part in self.partitions if part.kind == kind), None)


@dataclass(frozen=True)
class PlanValidation:
    valid: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]


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


def custom_plan(
    disk_size_mib: int,
    partitions: tuple[PartitionSpec, ...] = tuple(),
    changes: tuple[PartitionChange, ...] = tuple(),
) -> PartitionPlan:
    if disk_size_mib <= 0:
        raise BuilderError("Disk size must be positive.")
    plan = PartitionPlan(LayoutMode.CUSTOM, disk_size_mib, partitions, changes)
    validation = validate_plan(plan)
    if not validation.valid:
        raise BuilderError("Invalid custom partition plan: " + "; ".join(validation.errors))
    return plan


def validate_plan(plan: PartitionPlan) -> PlanValidation:
    errors: list[str] = []
    warnings: list[str] = []

    if plan.disk_size_mib <= 0:
        errors.append("Disk size must be positive.")

    sized_total = sum(part.size_mib or 0 for part in plan.partitions)
    if sized_total > plan.disk_size_mib:
        errors.append("Planned partitions exceed the physical disk size.")

    if plan.mode == LayoutMode.CUSTOM:
        windows = [part for part in plan.partitions if part.kind == "windows"]
        esp = [part for part in plan.partitions if part.kind == "esp"]
        recovery = [part for part in plan.partitions if part.kind == "recovery"]
        msr = [part for part in plan.partitions if part.kind == "msr"]

        if plan.partitions:
            if len(windows) != 1:
                errors.append("Custom layout must select exactly one FX11 / Windows target partition.")
            if len(esp) != 1:
                errors.append("UEFI installation requires exactly one selected EFI System Partition.")
            if len(windows) == 1:
                target = windows[0]
                if (target.filesystem or "").upper() != "NTFS":
                    errors.append("FX11 / Windows target must use NTFS.")
                if (target.size_mib or 0) < FX11_MIN_WINDOWS_GIB * 1024:
                    warnings.append(
                        f"FX11 target is smaller than the recommended {FX11_MIN_WINDOWS_GIB} GiB guided minimum."
                    )
            if len(esp) == 1 and (esp[0].filesystem or "").upper() != "FAT32":
                errors.append("Selected EFI System Partition must use FAT32.")
            if not recovery:
                warnings.append("No Windows Recovery partition selected; WinRE functionality may be reduced.")
            if not msr:
                warnings.append("No MSR selected; FX11 recommends the standard Windows GPT layout.")
            if len(recovery) > 1:
                errors.append("Select at most one Windows Recovery partition for FX11.")

    for change in plan.changes:
        if change.action in {ChangeKind.DELETE, ChangeKind.RESIZE, ChangeKind.FORMAT, ChangeKind.PRESERVE}:
            if change.partition_number is None or change.partition_number <= 0:
                errors.append(f"{change.action.value} requires an existing partition number.")
        if change.action == ChangeKind.CREATE and (change.size_mib is None or change.size_mib <= 0):
            errors.append("create requires a positive partition size.")
        if change.action == ChangeKind.RESIZE and (change.size_mib is None or change.size_mib <= 0):
            errors.append("resize requires a positive target size.")
        if change.action == ChangeKind.FORMAT and not change.filesystem:
            errors.append("format requires a filesystem.")

    return PlanValidation(not errors, tuple(errors), tuple(warnings))


def diskpart_script(plan: PartitionPlan, disk_number: int) -> str:
    if plan.mode == LayoutMode.CUSTOM:
        raise BuilderError("Use custom_diskpart_script() for a staged Custom plan.")
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
    return "\r\n".join(lines) + "\r\n"


def custom_diskpart_script(plan: PartitionPlan, disk_number: int) -> str:
    if plan.mode != LayoutMode.CUSTOM:
        raise BuilderError("custom_diskpart_script() requires a Custom partition plan.")
    if disk_number < 0:
        raise BuilderError("Disk number must be selected explicitly.")
    validation = validate_plan(plan)
    if not validation.valid:
        raise BuilderError("Invalid custom partition plan: " + "; ".join(validation.errors))

    if any(change.action == ChangeKind.RESIZE for change in plan.changes):
        raise BuilderError(
            "Resize requires the size-aware WinPE executor; refusing to emit an ambiguous DiskPart resize command."
        )

    lines = [f"select disk {disk_number}"]
    for change in plan.changes:
        if change.action == ChangeKind.PRESERVE:
            continue
        if change.action == ChangeKind.DELETE:
            lines.extend([f"select partition {change.partition_number}", "delete partition override"])
        elif change.action == ChangeKind.FORMAT:
            label = f' label="{change.label}"' if change.label else ""
            lines.extend(
                [
                    f"select partition {change.partition_number}",
                    f"format quick fs={change.filesystem.lower()}{label}",
                ]
            )
        elif change.action == ChangeKind.CREATE:
            kind = (change.kind or "primary").lower()
            if kind == "esp":
                lines.append(f"create partition efi size={change.size_mib}")
            elif kind == "msr":
                lines.append(f"create partition msr size={change.size_mib}")
            else:
                lines.append(f"create partition primary size={change.size_mib}")
            if change.filesystem:
                label = f' label="{change.label}"' if change.label else ""
                lines.append(f"format quick fs={change.filesystem.lower()}{label}")
            if kind == "recovery":
                lines.extend(
                    [
                        "set id=de94bba4-06d1-4d40-a16a-bfd50179d6ac",
                        "gpt attributes=0x8000000000000001",
                    ]
                )

    return "\r\n".join(lines) + "\r\n"
