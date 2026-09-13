# FX11 Live as a possible future FX Linux foundation

Date: 2026-09-14

Decision:

The new FX11 installation architecture uses a Linux Live environment as the primary visible installation shell. FX11 Installer runs there, owns disk selection and partitioning, and uses GParted only as an advanced/custom partitioning tool. WinPE remains the native Windows deployment engine after the Linux-side preparation phase.

This Linux Live environment may become a useful technical foundation for a future sibling product, FX Linux.

Important boundary:

- FX11 Builder remains a Windows-image builder and Windows installation project.
- FX Linux, if created, should remain a separate product/repository.
- Shared components may later be extracted or reused deliberately: boot environment, installer shell, disk detection, partition workflow, FX branding, recovery/diagnostics and multi-OS logic.
- Do not design the current FX11 Live environment around speculative FX Linux requirements at the expense of finishing FX11.

Rationale:

Building a polished Linux Live shell for FX11 naturally creates infrastructure similar to what a Linux distribution installer/live medium would need. Reuse is attractive, but product boundaries and upstream licensing/provenance must remain explicit.

Current priority:

Finish the FX11 Live installer flow first. Treat possible FX Linux reuse as an architectural advantage, not as a second active product scope.
