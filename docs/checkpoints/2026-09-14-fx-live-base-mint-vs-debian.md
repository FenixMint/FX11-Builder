# FX Live base: Mint vs Debian — evaluation checkpoint

Date: 2026-09-14

## Context

FX11 installation architecture is moving away from using GParted Live as the main environment. The new direction is a dedicated Linux Live environment that launches the FX11 Installer, with GParted available only as an advanced/custom partitioning tool. WinPE remains the native execution environment for final Windows deployment (DISM, BCDBoot, WinRE).

## Current evaluation

Linux Mint is being considered as a higher-level base because it already provides a mature desktop/live experience and reduces the amount of low-level integration work compared with building directly from a minimal Debian Live image.

The strongest candidate in this family is LMDE rather than the Ubuntu-based Linux Mint edition:

- LMDE uses Debian as its package base, preserving the desired Debian foundation.
- It provides the Mint desktop/user-experience layer and Mint tooling without requiring Ubuntu as the underlying distribution.
- It is therefore a useful bridge between a clean Debian base and a more complete, user-friendly live environment.

The Ubuntu-based Linux Mint line remains useful as a reference for UX, hardware support and installer behavior, but choosing it as the FX Live base would introduce an Ubuntu dependency that is not obviously necessary for the long-term FX architecture.

## Important constraints

- FX must not redistribute a modified Mint ISO while presenting it as Linux Mint.
- Any derived live image must use FX branding and clearly credit upstream components.
- A direct remaster of an upstream Mint/LMDE ISO may be fast for prototyping but should not automatically become the long-term build architecture. Reproducible builds and clear ownership of FX-specific layers are still desired.
- LMDE's own installer is not assumed to be reusable as the FX11 installer; FX11 needs its own orchestration and partition validation flow.
- LMDE 7 currently has some open installer issues, so its installer implementation should be treated as reference material rather than trusted wholesale.

## Decision status

No final base selection yet.

Current preference to validate next:

**LMDE / Debian + Mint layer** as the first serious candidate for FX Live, because it combines Debian foundations with a more complete live desktop stack and can also inform a future, separate FX Linux project.

Pure Debian Live remains the cleanest and most controllable fallback if Mint-layer coupling proves too heavy or fragile.
