from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from .iso import BuilderError, run_checked, sha256_file
from .winpe import (
    CustomizedBootWim,
    _read_boot_image_index,
    winpe_update_commands,
    write_winpe_payload,
)


def customize_boot_wim_file(source_boot_wim: Path, work_root: Path) -> CustomizedBootWim:
    """Customize a boot.wim that has already been extracted from source media."""
    source_boot_wim = source_boot_wim.expanduser().resolve()
    if not source_boot_wim.is_file():
        raise BuilderError(f"Source boot.wim not found: {source_boot_wim}")

    work_root = work_root.expanduser().resolve()
    work_root.mkdir(parents=True, exist_ok=True)
    boot_wim = work_root / "boot.wim"
    shutil.copy2(source_boot_wim, boot_wim)

    source_hash = sha256_file(boot_wim)
    image_index = _read_boot_image_index(boot_wim)
    payload = write_winpe_payload(work_root / "payload")
    commands = winpe_update_commands(payload)

    proc = subprocess.run(
        [
            "wimlib-imagex",
            "update",
            str(boot_wim),
            str(image_index),
            "--check",
            "--rebuild",
        ],
        input=commands.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or b"").decode("utf-8", errors="replace").strip()
        raise BuilderError(f"Unable to inject FX11 startup into boot.wim image {image_index}.\n{detail}")

    run_checked(["wimlib-imagex", "verify", str(boot_wim)])
    output_hash = sha256_file(boot_wim)
    if output_hash == source_hash:
        raise BuilderError("boot.wim hash did not change after FX11 WinPE customization.")

    return CustomizedBootWim(
        path=boot_wim,
        image_index=image_index,
        source_sha256=source_hash,
        output_sha256=output_hash,
        payload=payload,
    )
