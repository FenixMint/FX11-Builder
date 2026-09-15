# FX Base Live mode decision — 2026-09-15

Decision confirmed by user:

- FX Base is a bootable Live environment, analogous in behavior to LMDE Live.
- The same Live root filesystem is the common runtime foundation for FX Linux and FX11 installer flows.
- Boot menu entries select intent via kernel parameters rather than separate Live images:
  - `fx.mode=windows` -> FX11 installation path
  - `fx.mode=linux` -> FX Linux installation path
  - `fx.mode=live` -> normal FX Base / FX Linux Live session and tools
- `Try FX / Tools` is the normal Live session equivalent of LMDE's live boot.
- The first implementation goal is to preserve the proven LMDE live-boot mechanism while replacing user-facing branding, menu and routing with FX components.
- FX Base is the common platform, not a third end-user product line by itself.

This checkpoint refines the earlier FX Base architecture and makes the Live behavior explicit.
