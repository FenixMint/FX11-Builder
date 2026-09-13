# QEMU real ISO — GParted reached, interactive keymap prompt observed

Date: 2026-09-13

Observed on the real FX11 Home ISO in QEMU/OVMF:

- OVMF starts the FX11 media.
- FX GRUB takes over successfully.
- The default `FX Partition Manager — powered by GParted` entry starts the nested pinned GParted Live ISO.
- GParted Live progresses far enough to show Debian `console-data` package configuration.
- An interactive keymap policy dialog is displayed with options including `Don't touch keymap`.

Interpretation:

- The important UEFI/GRUB/nested-ISO handoff is working in the real build.
- The current media boot parameters do not yet suppress all GParted Live keyboard/locale setup prompts.
- This is an UX issue, not evidence that the GParted handoff failed.
- For the current test, selecting `Don't touch keymap` is the safest path to continue without changing the test VM keyboard mapping.

Follow-up:

- determine the correct GParted Live boot parameters/preseed for a non-interactive FX Partition Manager startup,
- keep the normal upstream GParted application visible and attributed,
- avoid adding brittle UI automation; prefer documented boot parameters and deterministic configuration.

Do not claim the graphical GParted desktop as fully reached until it is actually observed.
