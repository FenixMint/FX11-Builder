# FX Partition Manager — GParted Mainline Integration

Status: canonical mainline partitioning direction as of 2026-09-13.

## Decision

The primary graphical partitioning experience for FX11 will be based on a customized GParted Live environment.

User-facing product name:

**FX Partition Manager**

Attribution visible in the UI and/or About screen:

**powered by GParted**

The existing FX11 text-mode partition manager remains in the project as:

- an emergency fallback,
- a recovery path,
- a development/reference implementation,
- a future basis for native FX partitioning logic where it is useful.

It is not deleted.

## Why GParted becomes the mainline path

GParted already provides mature graphical handling of operations that are risky and expensive to reimplement correctly, including:

- partition creation/deletion,
- moving/resizing partitions,
- NTFS resizing,
- FAT32/ESP handling,
- broad Linux/BSD filesystem visibility,
- GPT partition-table management,
- multi-disk inspection,
- staged operations and explicit Apply behavior.

This fits the FX11 product principle:

**Your System. Your Rules.**

and avoids turning FX Partition Manager into a fragile custom partition editor before the rest of the installer is mature.

## High-level boot flow

Target installation-media flow:

`UEFI -> FX boot menu -> FX Partition Manager (custom GParted Live) -> partition validation -> Continue FX11 installation -> WinPE -> FX11 Installer -> direct image deployment -> Windows boot files -> FX Boot Manager -> OOBE`

The current unsigned development FX Boot Manager still assumes Secure Boot OFF.

## UX model

The customized GParted Live environment should boot into an FX-branded front end rather than exposing a generic live desktop first.

The front end should present:

- **FX11 only**
- **FX11 + Other OS**
- **Custom**

Guided modes may be implemented by FX scripts using deterministic partitioning tools available in the live environment.

Custom mode opens the full GParted GUI.

Suggested wording:

- `Open advanced partition editor`
- `powered by GParted`

The upstream GParted application identity should remain visible in an About/credits context. FX11 must not falsely claim authorship of GParted or imply upstream endorsement.

## Guided layouts

Canonical UEFI/GPT guided layout remains:

`EFI System -> MSR -> FX11 / Windows -> Windows Recovery`

Current defaults remain:

- ESP: 300 MiB FAT32
- MSR: 16 MiB
- FX11/Windows target: NTFS
- Recovery: at least 1024 MiB with the existing FX11 recovery-sizing rules
- Other OS space in guided multi-OS mode remains unallocated

The term **Other OS** remains canonical. Do not rename this to Linux.

## Validation after GParted

Closing GParted is not sufficient to start installation automatically.

FX11 must re-scan the disk state and validate that the layout is usable.

At minimum validate:

- selected physical disk is identifiable,
- usable GPT layout for the current UEFI path,
- one intended FX11/Windows target exists,
- target filesystem is NTFS or can be intentionally formatted to NTFS,
- a usable FAT32 EFI System Partition exists,
- sufficient capacity for the selected Windows image,
- Recovery is present when selected/recommended,
- no ambiguous target selection exists.

Only then enable:

**Continue to FX11 installation**

## Linux-to-WinPE handoff

Do not rely on Linux device names such as `/dev/sda` surviving as Windows `Disk 0`.

The GParted/FX environment should write a machine-readable installation context using stable evidence such as:

- GPT partition GUIDs,
- filesystem UUIDs where appropriate,
- partition type GUIDs,
- disk identity/model/size,
- an FX-generated install transaction ID.

Preferred development handoff locations:

ESP:

`/EFI/FX11/install-context.json`

`/EFI/FX11/install-ready`

and optionally an FX marker on the intended Windows target.

The handoff should contain one randomly generated `install_id` shared by all markers for that install transaction.

WinPE must rediscover partitions and match them against the stable IDs rather than trusting Linux enumeration order.

## Continue-to-install behavior

After partition validation, the user chooses **Continue to FX11 installation**.

Preferred behavior:

1. write the validated install context,
2. sync/unmount cleanly,
3. select/set the installation continuation path,
4. reboot into the WinPE stage,
5. WinPE verifies the install context and selected partitions,
6. FX11 Installer proceeds without asking the user to repeat disk choices.

The existing WinPE text partition manager remains accessible only as fallback/recovery once this path is mature.

## Boot-media architecture

The FX11 installation ISO will become a multi-environment image containing both:

- the FX Partition Manager Linux environment,
- the Microsoft WinPE/Windows deployment environment from the user's source Windows ISO.

FX-controlled GRUB is the natural top-level boot selector for this development architecture.

Expected entries during development may include:

- `Install FX11` / `FX Partition Manager`
- `Continue FX11 installation` when a valid install context exists
- `FX11 WinPE recovery / text fallback`
- `Windows Setup fallback` only as an explicit recovery option

## Branding

Branding targets include:

- FX boot splash/menu,
- FX Lazur background,
- FX logo,
- `FX Partition Manager` title,
- FX color/theme choices,
- localized labels,
- automatic startup of the FX front end,
- hiding unnecessary generic live-desktop clutter where safe.

Do not alter GParted behavior in ways that make destructive actions less obvious.

## Licensing and attribution

GParted is distributed under GNU GPL version 2 or, at the user's option, any later version.

FX11 may modify and redistribute GParted/GParted Live provided the redistribution satisfies the applicable GPL requirements and the licenses of all included third-party components.

Release requirements for any redistributed modified GParted-based image include at minimum:

- retain applicable copyright notices,
- include the applicable GPL license text,
- identify that GParted is third-party free software,
- make the corresponding source code for distributed GPL-covered binaries available in a GPL-compliant way,
- make FX modifications to GPL-covered components available under compatible terms where required,
- preserve notices/licenses for other included packages,
- document the exact upstream GParted Live version used,
- record hashes/provenance of imported upstream artifacts.

For FX11 public releases, the preferred compliance model is to publish alongside the binary release the source/patch/build information needed to satisfy applicable licenses, plus notices and hashes.

Do not treat the GPL as merely an attribution requirement; source-code obligations are part of redistribution compliance.

## Upstream modification strategy

Prefer the smallest possible delta from upstream GParted Live.

First phase:

- customize live environment,
- add FX front end/scripts,
- add branding assets,
- configure autostart,
- leave GParted application itself largely upstream.

Only fork/patch GParted application code if a real product requirement cannot be achieved cleanly around it.

This reduces maintenance and makes security/upstream updates easier.

## Security and update policy

GParted/GParted Live becomes a third-party supply-chain dependency and therefore must be tracked like a build input.

Builder/release engineering should record:

- upstream version,
- upstream download/source URL,
- SHA-256,
- included Linux kernel version,
- major partition/filesystem tooling versions where practical,
- FX patches,
- build date.

Do not download an unpinned `latest` live image and silently embed it into a release.

## Fallback FX text manager

The current native/text FX partition manager remains valuable.

Keep it for:

- emergency boot when the graphical environment fails,
- simple clean-disk guided layout,
- diagnostics,
- repair/recovery,
- future native implementation experiments,
- automated tests where launching GParted is inappropriate.

It should remain non-destructive by default until the user explicitly selects and confirms an operation.

## Immediate implementation sequence

1. Keep current WinPE/text installer path working as fallback.
2. Add pinned GParted Live source/import handling to FX11 Builder.
3. Build a custom FX Linux live payload with branding and an FX launcher.
4. Add top-level GRUB entries for FX Partition Manager and WinPE continuation.
5. Add stable partition discovery and `install-context.json` writer in the Linux stage.
6. Add matching context reader/validator in WinPE.
7. Implement guided FX11-only and FX11+Other-OS presets around GParted/parted/sgdisk.
8. Launch full GParted for Custom mode.
9. After GParted exits, validate the actual resulting disk layout.
10. Enable Continue to FX11 only after validation passes.
11. Keep the existing text partition manager available from an Advanced/Recovery path.
