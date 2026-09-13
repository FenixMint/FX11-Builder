# Checkpoint — synthetic E2E reached VALID, assertion diagnostics hardened

Date: 2026-09-13

## Local result on Linux Mint 22.3

The user updated to commit `964892bc41c123b65385b3a1241b59cddafe5519` and ran:

`PATH="$PWD/.venv/bin:$PATH" tests/e2e_synthetic.sh`

Observed result:

- synthetic Windows 11 Home/Pro WIM creation succeeded,
- FX11 inspection succeeded,
- Windows 11 Pro selection/export succeeded,
- `install.wim` verification succeeded,
- customized `boot.wim` verification succeeded,
- output ISO was produced successfully,
- `fx11 validate` reported `VALID`,
- the script did not reach the final `PASS` marker.

The local output ended immediately after `VALID: .../output.iso`, which means the remaining post-build WinPE payload content assertions still need to pass before synthetic E2E can be declared successful.

## Debian 13 CI result

GitHub Actions reproduced the same state on Debian GNU/Linux 13 (trixie):

- dependencies installed successfully,
- Python environment installed successfully,
- all 59 unit tests passed,
- `fx11 doctor` reported `STATUS: READY`,
- synthetic build reached `BUILD VALID` and `fx11 validate` reported `VALID`,
- the shell harness then exited with status 1 during post-build payload assertions.

This confirms that Debian 13 can run the FX11 Builder dependency/unit/doctor/build/validate path. The remaining failure is in the shell assertion layer after the ISO has already been built and validated, not in Debian package availability or core Builder execution.

## Fix

The E2E harness is changed to use explicit fixed-string, case-insensitive content assertions with named diagnostics. On any future mismatch it now prints:

- the failed assertion name,
- the expected literal,
- the file being checked,
- the actual file contents.

This removes fragile regular-expression/backslash handling from Windows path checks and makes a future failure directly diagnosable.

## Validation wording

Do not mark synthetic E2E as passed until the script prints exactly:

`FX11 synthetic end-to-end build with partition-to-installer handoff: PASS`

Do not mark a host as fully validated for genuine FX11 production builds until a genuine Microsoft Windows ISO has also completed the normal FX11 build and validation path on that host.
