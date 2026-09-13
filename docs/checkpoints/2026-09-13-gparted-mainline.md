# Checkpoint — GParted becomes mainline FX Partition Manager

Date: 2026-09-13

Decision accepted:

- Mainline graphical partitioning path will use a customized GParted Live environment branded as **FX Partition Manager**.
- Upstream attribution remains visible, using wording such as **powered by GParted**.
- The existing FX11 text partition manager is retained as emergency fallback, recovery path, test harness and future native-development track.
- The text manager is not deleted or abandoned.
- The main installation media will evolve into a multi-environment image: Linux/GParted for partitioning plus Microsoft WinPE for direct Windows deployment.
- After GParted/FX partitioning, FX validates the actual disk layout and writes a stable `install-context.json` handoff using GUID/UUID/disk identity data rather than trusting `/dev/sdX` versus Windows disk numbering.
- WinPE reads and verifies that handoff and continues directly to FX11 deployment without asking the user to choose the disk again.
- Current development Secure Boot policy remains Secure Boot OFF for the unsigned FX GRUB chain.
- GParted/GParted Live redistribution must satisfy GPL and all bundled third-party license obligations; upstream version and hashes must be pinned and recorded.
- Prefer customization around upstream GParted rather than a deep fork unless a real requirement forces application-level patches.

Canonical implementation spec:

`docs/FX_PARTITION_MANAGER_GPARTED.md`

License/compliance policy:

`docs/THIRD_PARTY_COMPLIANCE.md`

Immediate next engineering target:

1. keep current WinPE/text path bootable,
2. add pinned GParted Live import/build support,
3. create FX-branded live environment and launcher,
4. add GRUB flow between partitioning and WinPE continuation,
5. implement stable Linux-to-WinPE install-context handoff.
