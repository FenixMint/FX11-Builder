# Checkpoint — USB hybrid repack structurally valid

Date: 2026-09-13

Observed on the real FX11 Home test image after running `scripts/repack-fx11-usb-hybrid.sh`.

Input image:

- `FX11-25H2-PL-x64-Home-test2.iso`

Output image:

- `FX11-25H2-PL-x64-Home-test2-hybrid.iso`
- SHA-256: `dc1974de23274c253b773eb57c8bbff6c322e5f08e4d34eaceb76ad5b9ced27e`

Observed xorriso system-area result:

- Boot record: `El Torito , MBR protective-msdos-label cyl-align-off GPT`
- System area summary: `MBR protective-msdos-label cyl-align-off GPT`
- protective MBR present (`0xee`)
- GPT present
- GPT partition 2 named `EFI boot partition`
- GPT partition 2 points to `/efi/microsoft/boot/efisys.bin`
- GPT EFI partition size: 32768 x 512 bytes = 16 MiB

Observed El Torito result remains intact:

- BIOS boot image: `/boot/etfsboot.com`
- UEFI boot image: `/efi/microsoft/boot/efisys.bin`
- UEFI load size: 32768 x 512 bytes = 16 MiB

Script completed with:

`USB-HYBRID REPACK VALID`

Interpretation:

- The repacked image now has both optical-media El Torito metadata and a disk-style protective MBR + GPT with an EFI System Partition mapping.
- This resolves the previously observed structural gap where the ISO had El Torito but no System Area.
- This is a structural success only. Physical USB boot is not yet claimed until the hybrid ISO is written to USB, verified byte-for-byte, and actually booted on real UEFI hardware.

Next validation:

1. Raw-write the hybrid ISO to USB.
2. Verify the USB is byte-for-byte identical to the hybrid ISO.
3. Boot the USB on physical UEFI hardware with Secure Boot disabled.
4. Confirm FX GRUB appears.
5. Confirm FX Partition Manager / GParted starts from physical USB.
6. If successful, integrate hybrid generation directly into the normal `fx11 build` path and add tests/validation so the external repack helper is no longer required for normal builds.
