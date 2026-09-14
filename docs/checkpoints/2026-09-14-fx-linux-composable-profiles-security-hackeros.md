# FX Linux — composable profiles and security direction

Date: 2026-09-14
Status: architectural direction; not yet implemented

## Product model

FX Linux should remain one distribution, not a growing set of separate editions.
Installation features should be expressed as composable profiles / metapackages that can be selected together.

Examples:
- Standard
- Multimedia
- Gaming
- Security / Pentest
- later additional specialist profiles

Profiles may be combined, e.g. Standard + Multimedia + Gaming, or Standard + Security + Development. The installer must resolve duplicate packages and explicit conflicts rather than assuming profiles are mutually exclusive.

Desktop choice remains independent from functional profile choice. Planned desktop families: Cinnamon, MATE, KDE Plasma and TDE. FX Live / installer work starts with Cinnamon.

## Security profile

A dedicated hacker / security profile is wanted. Public-facing name should probably be `Security`, `Pentest` or similar rather than creating a separate Hacker edition.

Kali Linux is a primary reference for package grouping and workflow, but FX must not blindly import Kali as a base or mix Kali repositories into LMDE/Debian. Kali's metapackage model is useful: core/top tools plus domain groups such as information gathering, vulnerability assessment, web, wireless, password auditing, reverse engineering, exploitation, forensics, hardware, SDR, reporting, etc.

Preferred implementation model:
1. install host-native tools from Debian/LMDE repositories when practical;
2. package FX selections as our own metapackages such as `fx-security-core`, `fx-security-web`, `fx-security-wireless`, `fx-security-forensics`, etc.;
3. for Kali-specific or fast-moving tooling that would destabilize the host, use an isolated official Kali container (Podman/Distrobox-style) rather than mixing package repositories;
4. expose the result through a coherent FX Security UI / launcher later.

This preserves the stable LMDE/Debian host while still allowing a current Kali userland where useful.

## HackerOS assessment

HackerOS is a Polish Debian-based distribution with current Official, Cybersecurity, Gaming and other editions. Its current Cybersecurity direction is primarily Red-Team oriented. The project is worth studying selectively rather than adopting wholesale.

The most interesting HackerOS idea found so far is its `Penetration Mode` project. It uses a dedicated desktop application and isolates a BlackArch tool ecosystem in a Podman container instead of merging BlackArch repositories into the Debian host. The current project also includes an integrated terminal, activity/audit views, reports, settings/allowlist concepts and a tool store. This is architecturally relevant to FX Security because it demonstrates the same separation principle we want for Kali-specific tools.

The HackerOS Penetration-Mode repository currently carries an MIT license, so individual implementation ideas or code may be legally reusable subject to preserving the license notice where required. Nevertheless, the FX policy remains: understand first, select only what improves FX, and keep provenance explicit.

Other HackerOS elements such as a custom cybersecurity kernel, XEN, GhostFS, custom language and custom desktop are not assumed useful for FX. They require separate technical justification before adoption.

## Current FX profile model

Conceptual package layering:

```text
FX Base
├── desktop choice
│   ├── fx-desktop-cinnamon
│   ├── fx-desktop-mate
│   ├── fx-desktop-kde
│   └── fx-desktop-tde
│
├── fx-profile-standard
├── fx-profile-multimedia
├── fx-profile-gaming
└── fx-profile-security
    ├── fx-security-core
    ├── fx-security-web
    ├── fx-security-wireless
    ├── fx-security-forensics
    ├── fx-security-reversing
    ├── fx-security-hardware
    └── optional isolated Kali tool environment
```

The profile selector in Calamares should allow multiple selections and show disk-space impact / dependencies before installation.

## Guardrails

- Do not add Kali, Ubuntu or Arch/BlackArch repositories directly to the LMDE base.
- Prefer Debian packages and backports for host integration.
- Keep specialist rolling tool ecosystems isolated when this avoids dependency conflicts.
- Do not install every security tool by default.
- Profiles are user choices; "FX recommends; user decides."
- Security tooling is intended for authorized administration, research, education and penetration testing.
- Keep attribution and upstream licenses visible.

## Next research before implementation

Create a package/function matrix for:
- Kali current metapackages;
- Debian/LMDE availability of those tools;
- tools that genuinely require Kali packaging;
- HackerOS Penetration Mode concepts worth reproducing independently;
- conflicts between Gaming, Security, Multimedia and desktop profiles.

No ISO remaster work is scheduled as part of this checkpoint.