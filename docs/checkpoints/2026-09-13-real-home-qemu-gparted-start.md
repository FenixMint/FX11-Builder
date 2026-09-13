# Checkpoint — 2026-09-13 — real Windows 11 Home QEMU / FX GRUB / GParted start

## Observed runtime result

The real Windows 11 25H2 Polish x64 Home FX11 ISO was started with the current `fx11 test` QEMU/OVMF path on the HP 15-db0xxx development machine.

Observed by the user:

- UEFI boot reaches **FX GRUB**.
- FX GRUB has successfully taken over the installation-media UEFI boot path.
- The default/main entry starts **FX Partition Manager — powered by GParted**.
- GParted Live begins loading from the staged nested GParted ISO.
- Loading is slow on the current low-end HP test host, but the handoff from FX GRUB into GParted has been observed.

This is the first observed runtime confirmation of the intended real-media path:

`OVMF -> FX GRUB -> FX Partition Manager / GParted Live`

## What this proves

- the rebuilt real Microsoft 25H2 Home ISO is UEFI-bootable in QEMU/OVMF,
- the FX 16 MiB EFI El Torito image is actually executed,
- FX GRUB configuration is found and used,
- the GParted nested ISO path is found,
- GRUB reaches the GParted kernel/initrd launch stage.

## Still pending

Do not yet claim full GParted runtime success until the graphical GParted environment is fully up and usable.

Also still pending:

- complete GParted desktop startup confirmation,
- WinPE fallback runtime boot confirmation,
- partition-to-installer handoff,
- full Windows installation to the temporary VM disk,
- OOBE / SetupComplete / provisioning validation,
- installed-system runtime audit.

## Related real ISO

- edition: Windows 11 Home
- output: `FX11-25H2-PL-x64-Home-test2.iso`
- SHA-256: `4cb0b97e396441f6271c659a51245d89d8e6caaa0844f400edb90d04dc2936cd`
