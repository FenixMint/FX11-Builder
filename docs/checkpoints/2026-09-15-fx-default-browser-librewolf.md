# FX default browser: LibreWolf

Date: 2026-09-15

## Decision

- LibreWolf will be the default browser presented to users in FX Base / FX Linux.
- Firefox will remain installed initially and will not be removed during the first FX Base builds.
- Reason: preserve compatibility and avoid breaking package dependencies or desktop integrations before a reverse-dependency audit is completed.
- Default-browser behavior should point to LibreWolf (desktop launcher, MIME associations, xdg default browser where applicable).
- Firefox remains available as a compatibility fallback, but is not the primary FX browser.

## Validation before any Firefox removal

Before considering removal of Firefox in a later phase, validate on the actual FX Base package set:

- `apt-cache rdepends` / reverse dependency checks,
- desktop and MIME integration,
- packages that invoke `firefox` or depend on browser-related virtual packages,
- installer/live-session assumptions,
- upgrade behavior.

Do not remove Firefox merely to reduce duplication until the above is proven safe.

## Product intent

This follows the broader FX principle: choose privacy-respecting defaults while preserving compatibility and avoiding unnecessary breakage.
