# FX Live / future FX Linux release model notes — 2026-09-14

## Context

The discussion moved from the immediate FX11 installer architecture toward the Linux Live base that will host the FX11 Installer and could later seed a separate FX Linux project.

## Observations

- The user has long experience with Ubuntu-based Linux Mint and now uses LMDE in daily use.
- In normal desktop use the practical difference has felt small.
- One clearly noticed gap is `mintdrivers` / Driver Manager on LMDE.
- This is expected: Linux Mint's own developer documentation states that `mintdrivers` depends on the Ubuntu `ubuntu-drivers` backend and is not available in LMDE.
- LMDE 7 itself is not a rolling release; it is an LTS release based on Debian 13 Stable.
- Most Mint desktop tooling is nevertheless present in LMDE (e.g. mintinstall, mintupdate, mintreport, mintlocale, XApps/Cinnamon stack), while Ubuntu-specific hardware enablement / driver tooling is the more obvious gap.

## Release-model direction under consideration

The user prefers a rolling or continuous-release experience because it would avoid producing a new product release every ~6 months.

Important distinction for FX:

- a *rolling user-facing delivery model* does not require making every low-level system component rolling;
- for an installer/recovery environment, a stable and pinned storage/boot core is more valuable than blindly tracking Debian Testing/Unstable;
- FX can instead publish continuously refreshed ISO snapshots while keeping the critical core pinned and selectively updating kernel, firmware, Cinnamon/Mint userland, FX tools and applications.

Potential future model:

```
Debian Stable / LMDE-compatible core
        +
Mint/Cinnamon userland
        +
selected newer kernel / firmware / backports
        +
FX packages and branding
        =
FX Live continuous snapshots
```

This provides much of the operational convenience the user wants from rolling release without mixing Ubuntu binary repositories into Debian or exposing the installer stack to continuous ABI churn.

## Package policy

Do NOT mix Ubuntu Noble repositories directly into an LMDE/Debian base.

If an Ubuntu-based Mint component is valuable:

1. prefer an equivalent Debian package or backport;
2. otherwise use upstream/Mint source and rebuild/port against the Debian/LMDE base;
3. isolate non-system applications when practical;
4. treat driver-management functionality as a separate FX design problem rather than importing the Ubuntu driver stack wholesale.

## Status

No final base or release model is locked yet. LMDE/Debian remains the leading direction for FX Live. Continuous/rolling-style delivery is a design goal to evaluate separately from the choice of Debian Stable vs Testing.
