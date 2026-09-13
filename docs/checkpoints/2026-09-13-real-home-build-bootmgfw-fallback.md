# Checkpoint — 2026-09-13 — first real Windows 11 Home build fallback failure

## Observed on real Microsoft Windows 11 25H2 Polish x64 media

Source:
- `/home/hype/Pobrane/Win11_25H2_Polish_x64_v2.iso`
- SHA-256: `9453d410298e50c36ce31153326857848256e0980ff8fda501b4d3817540beb9`
- source media detected as UDF
- selected edition: `Windows 11 Home`, source image index 1
- GParted Live input had already verified against the pinned SHA-256

The real build progressed through the expensive parts successfully:
- selected Home image export completed
- generated single-image `install.wim` reached 6438 MiB integrity-table verification
- customized WinPE `boot.wim` verified successfully

The build then stopped before ISO creation with:

`ERROR: Microsoft bootmgfw.efi is missing from the UDF source; cannot keep the WinPE fallback while FX GRUB owns /efi/boot/bootx64.efi.`

No FX11 output ISO was produced, so subsequent `validate`, `audit`, and `test` correctly failed with `ISO not found` / `Output ISO is missing`.

## Root cause

The UDF repack path introduced an unnecessary dependency on `/efi/microsoft/boot/bootmgfw.efi` after changing `/efi/boot/bootx64.efi` into the FX GRUB filesystem fallback.

The source media is already known to contain Microsoft's `/efi/boot/bootx64.efi`. For optical El Torito boot, FX GRUB is supplied through the replacement EFI El Torito image (`/efi/microsoft/boot/efisys.bin`). Therefore the clean ISO architecture is:

- EFI El Torito image -> FX GRUB
- normal ISO filesystem `/efi/boot/bootx64.efi` -> keep original Microsoft loader unchanged
- FX GRUB WinPE fallback -> chainload the preserved `/efi/boot/bootx64.efi`

This avoids requiring `bootmgfw.efi` and avoids relocating a Microsoft loader.

## Important distinction

This decision is for the bootable ISO path. A future USB-media writer may intentionally install FX GRUB at the removable-media path `/EFI/BOOT/BOOTX64.EFI`; that is a separate media-generation problem and must not force the ISO path to overwrite Microsoft's filesystem loader.

## Status

- Real Home build: **FAILED at UEFI fallback staging**
- WIM export/integrity stage: **observed working**
- WinPE customization: **observed working**
- ISO generation: **not reached**
- QEMU/OVMF boot: **not reached**
- fix: retain Microsoft `/efi/boot/bootx64.efi` on UDF ISO builds and use it as the explicit WinPE fallback

Do not claim the real 25H2 Home ISO build works until the corrected build completes and the resulting ISO passes validation and OVMF/QEMU boot tests.
