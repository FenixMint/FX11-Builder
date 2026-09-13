from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .iso import BuilderError
from .partitioning import LayoutMode


SCHEMA = "fx11-install-context-v1"


@dataclass(frozen=True)
class PartitionRef:
    disk_number: int
    partition_number: int
    volume_id: str | None = None
    label: str | None = None


@dataclass(frozen=True)
class InstallContext:
    layout_mode: LayoutMode
    disk_number: int
    disk_model: str
    disk_size_mib: int
    windows: PartitionRef
    esp: PartitionRef
    recovery: PartitionRef | None = None
    preserved: tuple[PartitionRef, ...] = tuple()
    other_os_unallocated_mib: int = 0
    acknowledged_warnings: tuple[str, ...] = tuple()


def validate_install_context(context: InstallContext) -> None:
    if context.disk_number < 0:
        raise BuilderError("Install context requires an explicit physical disk number.")
    if context.disk_size_mib <= 0:
        raise BuilderError("Install context requires a positive physical disk size.")
    if not context.disk_model.strip():
        raise BuilderError("Install context requires the physical disk model.")
    for name, ref in (("FX11 target", context.windows), ("EFI System Partition", context.esp)):
        if ref.disk_number < 0 or ref.partition_number <= 0:
            raise BuilderError(f"{name} reference is invalid.")
    if context.windows.disk_number != context.disk_number:
        raise BuilderError("FX11 target must belong to the selected installation disk.")
    if context.esp.disk_number != context.disk_number:
        raise BuilderError("EFI System Partition must belong to the selected installation disk.")
    if context.recovery is not None and context.recovery.disk_number != context.disk_number:
        raise BuilderError("Recovery partition must belong to the selected installation disk.")
    if context.other_os_unallocated_mib < 0:
        raise BuilderError("Other OS unallocated size cannot be negative.")


def install_context_dict(context: InstallContext) -> dict[str, object]:
    validate_install_context(context)
    data = asdict(context)
    data["schema"] = SCHEMA
    data["layout_mode"] = context.layout_mode.value
    return data


def write_install_context(context: InstallContext, path: Path) -> Path:
    target = path.expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(install_context_dict(context), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def read_install_context(path: Path) -> InstallContext:
    target = path.expanduser().resolve()
    if not target.is_file():
        raise BuilderError(f"Install context not found: {target}")
    data = json.loads(target.read_text(encoding="utf-8"))
    if data.get("schema") != SCHEMA:
        raise BuilderError("Unsupported FX11 install context schema.")

    def ref(value: dict[str, object] | None) -> PartitionRef | None:
        if value is None:
            return None
        return PartitionRef(
            disk_number=int(value["disk_number"]),
            partition_number=int(value["partition_number"]),
            volume_id=value.get("volume_id"),
            label=value.get("label"),
        )

    context = InstallContext(
        layout_mode=LayoutMode(data["layout_mode"]),
        disk_number=int(data["disk_number"]),
        disk_model=str(data["disk_model"]),
        disk_size_mib=int(data["disk_size_mib"]),
        windows=ref(data["windows"]),  # type: ignore[arg-type]
        esp=ref(data["esp"]),  # type: ignore[arg-type]
        recovery=ref(data.get("recovery")),  # type: ignore[arg-type]
        preserved=tuple(ref(item) for item in data.get("preserved", []) if item is not None),  # type: ignore[arg-type]
        other_os_unallocated_mib=int(data.get("other_os_unallocated_mib", 0)),
        acknowledged_warnings=tuple(str(item) for item in data.get("acknowledged_warnings", [])),
    )
    validate_install_context(context)
    return context
