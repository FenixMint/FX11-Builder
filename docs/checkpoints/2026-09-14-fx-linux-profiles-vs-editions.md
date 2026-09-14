# FX Linux — profiles vs editions

Date: 2026-09-14
Status: design decision / working direction

## Decision

FX Linux should prefer **one common system base with composable installation profiles** over maintaining many separate editions.

Profiles may be combined by the user, for example:

- Standard
- Multimedia
- Gaming
- Security / Pentest
- Development

Desktop environment is a separate axis from functional profiles:

- Cinnamon
- MATE
- KDE Plasma
- TDE

Example combinations:

- Cinnamon + Multimedia
- KDE + Gaming + Multimedia
- Cinnamon + Security + Development
- TDE + Standard

## Why profiles are preferred for FX Linux

The planned FX Linux variants share the same underlying Debian/LMDE base, package manager, kernel policy, driver framework, update mechanism and installer. The differences are mostly packages, capabilities, configuration and runtime tuning. In that situation, profiles avoid duplicated ISOs, duplicated QA and edition drift.

Functional profiles should be represented as FX metapackages and configuration policies where practical, e.g. `fx-profile-gaming`, `fx-profile-security`, `fx-media-extras`.

## Why distributions still ship multiple editions

Multiple editions remain useful when the differences are deeper than package selection or when operational simplicity for the user outweighs maintainer duplication. Common reasons include:

1. Different desktop environments or strongly different default UX.
2. Different kernels, driver stacks or hardware targets.
3. Mutable vs immutable / atomic system architecture.
4. Different release cadence or base repositories (e.g. Stable vs Testing).
5. Offline-install requirements where the ISO must already contain all packages for a specific use case.
6. Strongly different security defaults, service sets or filesystem layout.
7. Marketing / onboarding simplicity: users can download a clearly named image instead of selecting options during installation.
8. QA predictability: a fixed image has a known package set and smaller combination matrix.

## FX Linux policy

For now, avoid multiplying editions. Use profiles where the base remains compatible and shared.

A future separate edition/flavor is justified only when a profile would need a materially different system base or boot/runtime architecture, such as:

- an immutable/atomic FX Linux variant,
- a significantly different kernel/driver stack,
- a special appliance/live environment,
- an offline image where bundled content materially differs,
- or another divergence that cannot be expressed cleanly as packages + configuration + runtime mode.

Desktop environments may eventually be distributed as separate installation media if ISO size, offline installation or QA makes that useful, but this is not the current plan.

## Important design principle

Do not confuse **profiles** with always-on tuning. A profile may install packages and capabilities, while runtime tuning should activate only when needed. Example: gaming performance tuning should not permanently force the entire system into a high-performance state.

## Current direction

One FX Linux platform, one installer, composable profiles, selectable desktop environment. Add separate editions only when the underlying system genuinely diverges.
