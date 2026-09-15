# FX browser policy checkpoint — 2026-09-15

## Decision

FX browser lineup should follow the project rule: **FX recommends; user decides.**

- **LibreWolf** — primary/default FX browser.
- **Firefox** — remains installed as a compatibility/fallback browser. Do not remove it merely for cleanup.
- **ungoogled-chromium** — optional second-engine browser (Chromium family) for users who want a Chromium-compatible browser with Google integrations reduced.
- **Brave** — optional browser choice.
- **Tor Browser** — optional specialist/privacy browser; not a default daily-browser replacement.

## Rationale

The goal is not to ship many browsers by default, but to provide a clear recommendation plus optional alternatives. LibreWolf remains the FX recommendation. Keeping Firefox avoids unnecessary disturbance to the LMDE/Mint package set and provides a useful compatibility fallback.

A second browser engine is valuable because LibreWolf/Firefox use Gecko, while ungoogled-chromium and Brave use Chromium/Blink. Tor Browser serves a different privacy/anonymity use case and should be presented separately from ordinary browsing choices.

## Verified LMDE 7 Firefox dependency observation

On the inspected LMDE 7 Cinnamon ISO, `apt-get -s remove firefox` proposed removing only:

- `firefox`
- `mintchat`

`mintchat` has a hard dependency on `firefox`. The test did not show `mint-meta-cinnamon` or `mint-meta-core` being removed as a direct consequence.

## UX direction

Do not preinstall every optional browser into the base image unless later image-size and maintenance testing justifies it. Preferred direction is:

1. ship LibreWolf as default;
2. keep Firefox installed;
3. expose ungoogled-chromium, Brave and Tor Browser as explicit optional installs/profiles or installer choices;
4. do not rebrand third-party browsers as FX products.
