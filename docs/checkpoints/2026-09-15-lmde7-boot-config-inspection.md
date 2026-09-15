# LMDE 7 boot configuration inspection — 2026-09-15

Source image:
- file: `lmde-7-cinnamon-64bit.iso`
- local test path: `/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`
- SHA256: `520b9de3e06871d69292f0e82a5979b62088ad83fdf4dce1d19100118a7033e4`
- volume ID: `LMDE 7 Cinnamon 64-bit`

## Live payload

Confirmed paths:
- `/live/filesystem.squashfs`
- `/live/vmlinuz`
- `/live/initrd.lz`

## BIOS boot path

LMDE uses ISOLINUX/SYSLINUX for BIOS boot.

`/isolinux/isolinux.cfg`:
```text
default vesamenu.c32
include live.cfg
```

The actual live boot entries are in `/isolinux/live.cfg`.

Normal live entry:
```text
label live
    menu label Start LMDE
    menu default
    kernel /live/vmlinuz
    append boot=live live-config initrd=/live/initrd.lz live-media-path=/live quiet splash --
```

Compatibility mode adds:
```text
ramdisk_size=1048576 root=/dev/ram rw xforcevesa noapic noacpi nosplash irqpoll
```

OEM mode adds:
```text
oem-mode quiet splash
```

## UEFI boot path

LMDE uses GRUB for UEFI. Both architecture-specific GRUB stubs found during inspection source the same top-level configuration:

```text
source /boot/grub/grub.cfg
```

Therefore `/boot/grub/grub.cfg` is the main UEFI menu configuration that matters for FX Live menu changes.

Normal UEFI live entry:
```text
menuentry "Start LMDE 7 64-bit" --class linuxmint {
    set gfxpayload=keep
    linux /live/vmlinuz boot=live live-config live-media-path=/live findiso=${iso_path} quiet splash --
    initrd /live/initrd.lz
}
```

Compatibility mode uses the same extra parameters as BIOS plus `findiso=${iso_path}`.

OEM mode uses:
```text
linux /live/vmlinuz boot=live live-config live-media-path=/live findiso=${iso_path} oem-mode quiet splash --
initrd /live/initrd.lz
```

UEFI GRUB also exposes:
- Boot from next volume
- UEFI Firmware Settings
- Memory test

## FX consequence

For the first FX Live PoC we can preserve LMDE's original boot stack and inject the FX product mode as a kernel command-line parameter.

Planned modes remain:
- `fx.mode=windows`
- `fx.mode=linux`
- `fx.mode=live`

Implementation points:
- BIOS: edit `/isolinux/live.cfg`
- UEFI: edit `/boot/grub/grub.cfg`

The architecture-specific GRUB configs do not need independent menu edits because they source `/boot/grub/grub.cfg`.

The normal LMDE boot arguments should otherwise be preserved. In particular, keep `boot=live live-config live-media-path=/live`; for UEFI/loopback flow keep `findiso=${iso_path}` where LMDE currently uses it.

## Inspection-script note

The first inspection reused `/tmp/lmde7-boot-inspect`. Files extracted from the ISO inherited read-only directory/file modes, so a later `rm -rf` emitted many `Brak dostępu` messages. This was inspection-workspace noise, not a failure of the ISO or boot configuration.

For future read-only inspections, use a fresh temporary directory from `mktemp -d` instead of reusing a fixed path. This avoids ownership/mode cleanup noise and does not require `sudo`.

## Status

Boot configuration and injection points are now identified. No source ISO modification has been performed by this inspection.
