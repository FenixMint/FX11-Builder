# Firefox removal simulation on LMDE 7 source ISO

Date: 2026-09-15

Source ISO: `/home/hype/Pobrane/lmde-7-cinnamon-64bit.iso`

A read-only simulation was run inside the LMDE 7 SquashFS with a writable tmpfs mounted at `/tmp`:

```text
The following packages will be REMOVED:
  firefox mintchat
0 upgraded, 0 newly installed, 2 to remove and 0 not upgraded.
Remv mintchat [1.8]
Remv firefox [143.0.3~linuxmint1+gigi]
```

This confirms that in this LMDE 7 image `mintchat` has a hard dependency on `firefox`. Removing Firefox would therefore also remove Mint Chat. No wider desktop or Cinnamon metapackage removal was proposed by APT in this simulation.

Project decision:
- LibreWolf will be the default browser in FX Base / FX Linux.
- Firefox remains installed as a secondary / compatibility browser.
- Do not remove Firefox merely for cleanup or branding purposes.
- This keeps upstream package relationships intact and avoids unnecessary churn.
