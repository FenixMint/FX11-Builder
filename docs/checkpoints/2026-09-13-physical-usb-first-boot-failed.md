# Checkpoint — first physical USB boot attempt failed

Date: 2026-09-13

Observed on physical media:

- FX11 Home ISO had already booted successfully in QEMU/OVMF through FX GRUB into the GParted GUI.
- First USB write was made to Kingston DataTraveler 3.0 using raw `dd`.
- A subsequent `cmp` check reported a byte mismatch between the ISO and `/dev/sdb`, so that write cannot be treated as a verified copy.
- The resulting USB did not boot on physical hardware.
- User is now retrying the write using the Linux graphical `Disks` application (`Restore Disk Image`).

Interpretation:

- The failed physical boot is not yet sufficient evidence that the ISO itself is non-bootable from USB, because the first raw write was not byte-identical to the ISO.
- If the Disks-written USB verifies byte-identical and still does not boot, investigate hybrid USB boot structure/system area in the generated ISO rather than blaming the write method.
- Next diagnostic after a clean write: verify with `cmp`, inspect `xorriso -indev stdio:/dev/sdX -report_el_torito plain`, and if needed inspect `-report_system_area plain`.
