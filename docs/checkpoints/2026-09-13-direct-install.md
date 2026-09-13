# FX11 checkpoint — text Partition Manager to direct Installer

Date: 2026-09-13

This checkpoint records the first development path where the WinPE text-mode FX Partition Manager can continue directly into FX11 installation without handing control to stock Windows Setup.

## Development flow

`WinPE -> FX11 launcher -> FX Partition Manager -> FX11 Installer -> DISM /Apply-Image -> BCDBoot -> optional WinRE -> reboot/OOBE`

## Text-mode FX Partition Manager

Current development menu supports:

- `FX11 only` guided layout,
- `FX11 + Other OS` guided layout,
- `Custom / manual` DiskPart path,
- return to launcher.

Guided layouts require an explicit physical disk number and an explicit erase confirmation before DiskPart is executed.

### FX11 only

The selected disk is erased and converted to GPT. The development script creates:

- EFI System Partition, 300 MiB, FAT32, temporary letter `S:`,
- Microsoft Reserved partition, 16 MiB,
- FX11 / Windows NTFS partition using the available space,
- then shrinks the freshly created FX11 volume by 1024 MiB,
- Recovery partition, 1024 MiB, NTFS, temporary letter `R:`,
- FX11 / Windows target uses temporary letter `W:`.

The `shrink desired=1024` operation in this guided fresh-disk path means “shrink by 1024 MiB”, not “resize to a 1024 MiB target”. This does not supersede the rule that arbitrary Custom resize must use a size-aware executor.

### FX11 + Other OS

The selected disk is erased and converted to GPT. The user enters the desired FX11 size in GiB, minimum 64 GiB. FX11 creates ESP, MSR, the chosen Windows target, and a 1024 MiB Recovery partition. Remaining disk space is intentionally left unallocated for Other OS.

### Custom / manual

Custom development mode launches DiskPart without automatic clean/format. Before continuing, the user must assign:

- `S:` to the selected FAT32 EFI System Partition,
- `W:` to the selected NTFS FX11 / Windows target,
- optional `R:` to Recovery.

The final graphical Custom implementation and size-aware resize executor remain future work.

## Handoff to FX11 Installer

After a guided layout succeeds, the manager asks:

`Continue directly to FX11 installation?`

If confirmed, `X:\FX11\fx11-install.cmd` starts.

Custom mode can use the same installer after `S:` and `W:` are present.

## Current FX11 Installer development behavior

The installer:

1. verifies `W:` and `S:` exist,
2. locates the FX11 installation media by `FX11-manifest.json` and `sources\install.wim`,
3. asks again before applying the image,
4. applies the single selected image with `DISM /Apply-Image /Index:1 /ApplyDir:W:\`,
5. stages `SetupComplete.cmd`, `FX11.ps1`, and the FX11 manifest into the applied Windows image,
6. creates Windows UEFI boot files using `BCDBoot W:\Windows /s S: /f UEFI`,
7. copies the unsigned development FX Boot Manager payload to `S:\EFI\FX11`,
8. attempts WinRE setup when `R:` exists,
9. offers reboot or return to the manager.

## Important development limitation

FX Boot Manager files are staged on the ESP, but this checkpoint does **not** yet create/move a firmware NVRAM entry that makes FX Boot Manager the default UEFI loader. Windows Boot Manager remains the reliable first-boot path for the first real hardware installation test.

Secure Boot remains OFF for the current unsigned GRUB development payload.

## Validation status

Tests were updated to cover the new text manager and direct deployment scripts, and the synthetic E2E test now checks that both scripts are present inside `boot.wim`.

CI was intentionally stopped earlier by the user, so no CI pass is claimed for this checkpoint. The next authoritative validation is local `pytest`, synthetic E2E, real Microsoft ISO build, then QEMU/OVMF and real-hardware testing.

## Commits

- `85318d9ea86132df0b2f3ce50ce0bdfc4e9ee4b1` — Connect text partition manager to direct FX11 deployment
- `768c55fb962e88bd47f66de339a31b2ea94a8039` — Test text partition manager to installer handoff
- `d5799b0b18afa3420a337ce45955f07de96eddef` — Record direct FX11 WinPE deployment in build manifest
- `611b9e47d53431c2ae8fd94b5df086856ae4ca1f` — Verify partition-to-installer scripts in synthetic ISO
