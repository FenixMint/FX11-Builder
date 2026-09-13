# 2026-09-14 — Validate, stop, pivot, continue

Project operating principle confirmed after the physical USB v5 test and installer architecture review.

## Principle

FX11 development should not preserve an implementation path merely because work has already been invested in it.

When a real test exposes friction, complexity or an architectural mismatch, the correct sequence is:

1. stop the current iteration,
2. validate what actually worked and what failed,
3. keep the proven pieces,
4. change direction where the architecture is fighting the intended user experience,
5. resume development from the new validated baseline.

## Current application to FX11

The v5 physical test proved that:

- FX GRUB boots on real hardware,
- the graphical boot UX is improving,
- GParted Live can start automatically without the old graphics prompts,
- the direct GRUB-to-WinPE installer handoff still fails,
- adding a special "Continue to FX11 Installer" handoff inside GParted is not the desired final UX.

The project therefore pivots away from treating GParted as the first half of the installer.

The next architecture target is one coherent FX11 Installer running in a Linux Live environment. GParted becomes an integrated Custom partitioning tool launched by the parent installer and closed back into that same installer flow. Automatic layouts may later use deterministic partitioning tools directly. WinPE remains the hidden/native deployment engine for DISM, BCDBoot, WinRE and other Windows-specific finalization work.

The user should experience one installer, even if Linux and WinPE are separate implementation layers underneath.

## Consequence

Further effort should prioritize the unified parent-installer workflow instead of continuing to patch the old GParted -> marker -> reboot -> GRUB -> WinPE handoff as the primary UX.

Existing work is not discarded. GRUB takeover, graphical theme work, GParted integration, hybrid media support and WinPE deployment remain reusable components.
