# Checkpoint — physical USB write is exact, ISO lacks disk System Area

Date: 2026-09-13

## Observed physical-media result

The generated real FX11 Home ISO was written to a Kingston DataTraveler 3.0 USB stick using GNOME Disks after an earlier raw-write attempt was not byte-identical.

The second write was verified against the source ISO with `cmp` over the exact ISO byte length:

```text
OK: USB jest bitowo identyczne z ISO
```

Therefore the physical USB content is an exact byte-for-byte copy of the generated FX11 ISO.

## Boot result

The exact-copy USB did not boot on the physical test machine.

## xorriso evidence from the USB

`xorriso -indev stdio:/dev/sdb -report_system_area plain` reported:

```text
Boot record  : El Torito
Volume id    : 'FX11'
xorriso : NOTE : No System Area was loaded
```

`xorriso -indev stdio:/dev/sdb -report_el_torito plain` reported valid optical boot entries:

```text
El Torito catalog  : 374  1
El Torito cat path : /boot/boot.cat
El Torito boot img : 1 BIOS ... LBA 375
El Torito boot img : 2 UEFI ... LBA 377
El Torito img path : 1 /boot/etfsboot.com
El Torito img path : 2 /efi/microsoft/boot/efisys.bin
```

## Diagnosis

The output is bootable as optical/El-Torito media and already boots in QEMU/OVMF, but the rebuilt ISO currently has no disk System Area / partition map for direct raw-write USB boot.

The physical USB failure is therefore not attributable to a bad copy: the second write is byte-identical. The builder's UDF-repack path needs explicit hybrid UEFI USB disk metadata.

## Planned builder change

For the UDF-repack path, keep the existing BIOS and UEFI El Torito entries, but expose the first UEFI El Torito FAT image as an EFI System Partition in GPT using xorriso's supported EFI boot-partition mechanism (`-efi-boot-part --efi-boot-image`) or an equivalently validated appended ESP layout.

This path does not depend on an ISOLINUX isohybrid MBR and is appropriate for the current FX11 UEFI-first installation media. BIOS El Torito remains available for optical-media compatibility; direct USB support target is UEFI.

Validation must additionally inspect `-report_system_area plain` and require a real GPT/EFI System Partition for rebuilt UDF output before the ISO is declared USB-ready.

## Status

Confirmed:

- real ISO build succeeds;
- QEMU/OVMF -> FX GRUB -> GParted GUI succeeds;
- physical USB image written via GNOME Disks is byte-identical to ISO;
- El Torito BIOS + UEFI entries exist;
- no System Area exists;
- current exact-copy USB does not boot physically.

Not yet confirmed:

- rebuilt hybrid ISO has a GPT/ESP System Area;
- raw-write USB boots physically;
- physical WinPE fallback and Windows deployment.