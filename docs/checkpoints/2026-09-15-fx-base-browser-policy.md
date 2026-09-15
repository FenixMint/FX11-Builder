# FX Base browser policy — 2026-09-15

## Decision

FX Base will use **LibreWolf as the default browser** for the user-facing FX experience.

Firefox will **remain installed for now** as a compatibility/fallback browser. We will not remove it during the first FX Base builds until its package relationships and reverse dependencies in the LMDE 7 base are audited.

## Rationale

- LibreWolf matches the FX privacy-oriented product direction and should be the browser opened by default.
- Firefox is already part of the LMDE base and may be referenced by packages, desktop integration, MIME/default-browser handling, metapackages, or other components.
- Removing a base browser too early creates unnecessary risk for the initial FX Base PoC.
- Keeping Firefox installed does not prevent FX from presenting LibreWolf as the primary browser.

## Implementation direction

For the first FX Base builds:

1. Install/integrate LibreWolf.
2. Set LibreWolf as the default browser for HTTP/HTTPS and normal desktop browser actions.
3. Prefer LibreWolf in the FX desktop launcher/panel/menu defaults.
4. Keep Firefox installed and functional as a secondary/fallback browser.
5. Before any future decision to remove Firefox, inspect the exact LMDE 7 package name, dependencies, reverse dependencies, metapackage relationships, and desktop integration effects.

## Branding

LibreWolf is an upstream third-party project. FX will not rebrand LibreWolf as an FX-owned browser. Its upstream identity and licensing must be respected while FX configures it as the default browser.
