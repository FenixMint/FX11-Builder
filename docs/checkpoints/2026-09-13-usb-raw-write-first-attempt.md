# 2026-09-13 — first raw USB write attempt

Observed on Linux Mint test host with a Kingston DataTraveler 3.0 (~57.6 GiB) identified as `/dev/sdb` at the time of the test.

## Source artifact

FX11 ISO:

`FX11-25H2-PL-x64-Home-test2.iso`

Expected SHA-256 from the validated build:

`4cb0b97e396441f6271c659a51245d89d8e6caaa0844f400edb90d04dc2936cd`

The ISO had already passed `fx11 validate` and El Torito inspection, and QEMU/OVMF had already reached FX GRUB and the GParted GUI.

## USB write

The ISO was written to the Kingston USB device with raw `dd`. The write ran at roughly USB 2.0 speed (~30 MB/s). The desktop later auto-mounted the written ISO9660 filesystem as label `FX11`.

## Verification result

A byte-for-byte comparison was attempted with:

```bash
sudo cmp -n "$(stat -c%s "$OUT")" "$OUT" /dev/sdb
```

Observed result:

- source and USB **differed**
- first reported mismatch at byte `1912602625`
- therefore this first raw write must not be considered verified or suitable as a trusted installation medium

The mounted USB was visible as:

- model: `DataTraveler 3.0`
- transport: USB
- removable: yes
- filesystem detected: ISO9660
- label: `FX11`

This proves the ISO filesystem header was readable from the device, but not that the whole image was written correctly.

## xorriso note

Direct `xorriso -indev /dev/sdb ...` was rejected because xorriso treats raw `/dev` paths as caution-class devices unless explicitly addressed through stdio. The correct form for read-only structural inspection is:

```bash
sudo xorriso -indev stdio:/dev/sdb -report_el_torito plain
```

The xorriso refusal itself is not an FX11 image failure.

## Next action

1. Re-confirm the source ISO SHA-256.
2. Re-write the USB after unmounting it, preferably on a USB 3.x port.
3. Re-run byte-for-byte verification before any real-machine install attempt.
4. If repeated verified writes fail on the same stick, test another USB device before changing the FX11 image format.

Do not mark raw-dd USB boot support as validated until a byte-identical write and physical UEFI boot have both been observed.
