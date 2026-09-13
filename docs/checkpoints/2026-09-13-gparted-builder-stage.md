# Checkpoint — GParted input staged by FX11 Builder

Date: 2026-09-13

This checkpoint records the first implementation step of the GParted mainline path.

## Implemented

- Pin GParted Live `1.8.1-6` / amd64 by exact SHA-256.
- Verify a local GParted Live ISO before FX11 accepts it as a build input.
- Expose the pinned input through:
  - `fx11 gparted info`
  - `fx11 gparted verify <iso>`
- Add `--gparted-live <iso>` to `fx11 build`.
- When supplied, embed the exact verified upstream ISO at:
  - `/FX11/gparted/gparted-live-1.8.1-6-amd64.iso`
- Generate and embed an FX installation-media GRUB configuration at:
  - `/FX11/media/grub.cfg`
- The media GRUB menu is designed with:
  - `FX Partition Manager — powered by GParted` as default entry,
  - GParted Live loopback boot using the upstream-supported `findiso` model,
  - `FX11 Installer / WinPE fallback`,
  - UEFI Firmware Settings.
- Record GParted provenance, hash and branding policy in `FX11-manifest.json` when the input is present.
- Keep the existing text FX Partition Manager and WinPE path unchanged as fallback.

## Important current boundary

The GParted ISO and media GRUB config are now staged inside the generated FX11 ISO, but the Windows installation media still boots through the original Microsoft El Torito/UEFI path.

Therefore the graphical GParted path is **not yet the active first boot path**.

The next critical implementation step is to create an FX-controlled UEFI El Torito boot image/ESP that starts FX GRUB first and preserves a reliable chainload path to the Microsoft WinPE boot environment.

## Relevant commits

- `146e35f73dbf35d94d532bd42791161de1626bcb` — pin GParted Live provenance
- `4078e534c1c051c3c6ccdf09f7b152766701384e` — add pinned GParted verifier
- `3abf09cee61ae59816f5329598953ff24374cd6a` — test GParted verifier
- `575b6ecfbe130a6117f9dc5f0fb8bcfeef442eca` — add standalone verification helper
- `0b32991c1a729392ff7cfeb2983a2eac0b3bf67b` — stage verified GParted ISO in builds
- `0f833a7ec9ad8bd783d320eb635c72da130b1cd2` — add CLI support
- `bf9360a005b0f480d96163cf59311884fede5869` — add FX installation-media GRUB generator
- `ce046b61dd1e19105b8897520ded27a07869c6eb` — test media GRUB menu
- `393e7eb454d8ab1fbafef75829606c670794fdcb` — stage media GRUB config in FX11 builds

## Validation still required

No CI success is claimed for these commits. Local `pytest`, synthetic E2E and then a genuine Microsoft ISO build remain required before this checkpoint is considered validated.
