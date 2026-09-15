# FX Linux — Linux Mint/LMDE reuse and branding policy

Date: 2026-09-15

## Decision

FX Linux is a distinct operating system and product. It may reuse Linux Mint / LMDE technology and GPL/open-source components where the applicable licenses permit it, but it must not be presented or branded as Linux Mint or LMDE and must not imply affiliation with the Linux Mint project.

## Practical policy

- Use LMDE as a technical base/reference where useful, while keeping FX Linux identity independent.
- Replace Linux Mint / LMDE product branding in boot menus, artwork, wallpapers, installer identity, welcome screens, release strings, and other user-facing identity surfaces with FX branding.
- Do not call the resulting distribution Linux Mint or LMDE.
- Do not use Linux Mint logos or branded artwork as FX Linux product identity.
- Preserve required upstream copyright notices, license texts, source obligations, and attribution for reused software.
- Unmodified Mint-developed GPL software may be reused under its license; if FX modifies a Mint-developed program in a way that could confuse provenance/quality attribution, prefer renaming/forking the modified component and clearly crediting upstream.
- Do not mix this branding policy with package provenance: a package may retain its upstream package/project name where appropriate even though the operating system itself is FX Linux.
- Keep a third-party provenance/compliance record for Mint, Debian, Calamares, GRUB, Valve/SteamOS-inspired components, Kali/other profile sources, and other upstreams.

## Rationale

Linux Mint's official FAQ permits commercial use and sale but says users must not pretend to be Linux Mint or create the impression of affiliation. Linux Mint project guidance also distinguishes GPL-licensed Mint-developed software from protected Linux Mint names, logos, artwork, and product identity. Publicly distributed modified Mint/LMDE images therefore need independent naming and branding.

This matches the FX project direction: we are building our own system, not a rebranded claim of being Linux Mint. Upstream technology should be credited visibly and honestly.

## Note

This is an engineering/compliance policy for the project, not legal advice. Individual third-party components remain subject to their own licenses and trademark terms.
