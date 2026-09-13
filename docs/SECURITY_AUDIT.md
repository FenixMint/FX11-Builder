# FX11 Security Audit

Status: initial static review. This document is not a proof that software is free from vulnerabilities or malicious behavior. It records what was inspected, what was found, and what FX11 should harden before release.

## Scope

This first pass covers:

- the current `ntdevlabs/tiny11builder` repository as an upstream inspiration source,
- the current FX11 Builder source tree,
- build-time downloads and dependencies,
- Windows provisioning behavior,
- security-sensitive changes such as Defender, Windows Update, account creation, persistence and remote/network actions.

## Initial conclusion

No obvious backdoor was identified in the reviewed tiny11builder source or in FX11 Builder.

However, tiny11builder contains several patterns that FX11 should **not inherit blindly**. The most important risk is not an identified backdoor but a **software supply-chain problem**: upstream tiny11maker can fetch mutable content from the `main` branch at build time, and downloads an executable without independently pinning/verifying its expected hash.

FX11 is already substantially separated from that design: its current implementation is an independent Linux-native builder and does not copy or execute tiny11maker PowerShell code.

## Upstream tiny11builder review

Reviewed upstream tree: `ntdevlabs/tiny11builder`.

At the time of this review the repository contains a small, auditable set of source files: README, `autounattend.xml`, `tiny11maker.ps1`, `tiny11Coremaker.ps1` and funding metadata. No executable binary is stored directly in the current source tree.

### Good signs

No obvious examples were found of:

- obfuscated or Base64/EncodedCommand payloads,
- `Invoke-Expression` download-and-execute behavior,
- hidden user-account creation,
- scheduled-task persistence,
- Defender exclusion creation,
- obvious command-and-control endpoints,
- arbitrary third-party binary download domains in the normal maker path.

The current `autounattend.xml` is small and readable. It mainly affects OOBE/installation behavior and does not contain embedded scripts, credentials or hidden user creation.

### Finding T11-01 — mutable remote `autounattend.xml`

Severity: **High supply-chain risk**

`tiny11maker.ps1` downloads `autounattend.xml` from the upstream repository's `main` branch when the local file is absent.

Risk:

- `main` is mutable,
- a compromised upstream account/repository could alter that XML after the builder script was reviewed,
- an unattended Windows setup file is security-sensitive and can potentially execute configuration/actions during installation,
- the builder does not pin that download to a reviewed commit SHA or verify a known checksum.

This is not evidence that the current upstream file is malicious. It is a design that makes a future supply-chain compromise more dangerous.

**FX11 policy:** never download installation-time scripts/configuration from an unpinned branch during a build. All executable/configuration content injected into an ISO must come from the reviewed FX11 source revision or from a cryptographically verified trusted source.

### Finding T11-02 — downloaded `oscdimg.exe` without expected-hash verification

Severity: **Medium**

When the Windows ADK tool is unavailable, upstream tiny11builder downloads `oscdimg.exe` from a Microsoft download/symbol-server URL.

The domain is Microsoft-controlled, which reduces risk, but the script does not independently verify a pinned expected SHA-256 before executing the downloaded program.

**FX11 policy:** prefer locally installed distro packages/tools where possible. Any executable downloaded at runtime must have an explicit source policy plus signature and/or expected-hash validation before execution.

### Finding T11-03 — tiny11 Core disables important security/servicing controls

Severity: **High if inherited; informational for FX11**

`tiny11Coremaker.ps1` intentionally goes much further than the normal maker. Its documented behavior includes disabling Windows Defender and Windows Update and removing servicing/recovery components. It also uses RunOnce entries to keep Windows Update stopped after OOBE.

This is intentional functionality rather than a hidden backdoor, but it conflicts with FX11's security model.

**FX11 policy:** do not inherit tiny11 Core behavior. Preserve Microsoft Defender, Windows Update, SmartScreen, Windows Recovery, Windows Installer and normal servicing.

### Finding T11-04 — privileged PowerShell execution

Severity: **Expected / Medium operational risk**

Upstream scripts require administrative execution and modify PowerShell execution policy when needed. This is understandable for offline Windows image servicing, but means the scripts execute with enough privilege to alter the build host and image deeply.

**FX11 policy:** keep privileged operations minimal and explicit. The Linux builder should not request root privileges except for host package installation; ISO building itself should run as an ordinary user wherever possible.

## FX11 Builder review

### Current architecture

FX11 does not execute upstream tiny11builder scripts. It uses its own Python code, `wimlib-imagex`, `xorriso`, Windows SetupComplete provisioning and declared profiles.

The current runtime Python project has no third-party runtime Python dependencies. Development uses pytest, while system tools are installed from the Linux distribution repositories.

### Positive findings

Current FX11 code:

- hashes the source ISO with SHA-256,
- rechecks the source hash before and after the build,
- refuses to overwrite the source ISO,
- exports the selected Windows image instead of mutating the source image in place,
- writes an output SHA-256,
- includes a build manifest,
- keeps Defender, Windows Update, Store, SmartScreen, Edge/WebView2, Terminal and Recovery protected in the default design,
- uses argument arrays for external commands instead of shell-string construction,
- contains no current application-runtime network downloader in the ISO build path,
- contains no bundled executable blobs in the repository tree.

### Finding FX11-01 — SetupComplete uses `ExecutionPolicy Bypass`

Severity: **Low/Medium**

`SetupComplete.cmd` invokes the FX11 PowerShell provisioning script using `-ExecutionPolicy Bypass`.

This is common for controlled setup automation and the script is generated by FX11 itself, but it means PowerShell policy is not an integrity boundary for that file.

**Hardening action:** include SHA-256 values for every injected FX11 executable/script/configuration file in the build manifest and verify them before execution where practical. Long term, sign FX11 Windows-side scripts/binaries when a signing process exists.

### Finding FX11-02 — source ISO authenticity is not independently established

Severity: **Medium**

FX11 protects against the source ISO changing during a build, but a SHA-256 calculated locally does not prove that the original ISO came from Microsoft.

**Hardening action:** add an optional/strongly recommended source-verification stage. Record source provenance and, where Microsoft publishes trustworthy hashes or signatures that can be verified, validate them. At minimum warn when provenance is unknown.

### Finding FX11-03 — build-tool provenance

Severity: **Medium**

FX11 trusts `wimlib-imagex`, `xorriso`, Python and other host tools found on `PATH`. The bootstrap obtains them through the Debian/Mint package manager, which is preferable to random downloads, but the resulting manifest does not yet record their versions.

**Hardening action:** record exact versions and resolved executable paths of security-relevant build tools in the build manifest. Consider a reproducible/containerized build profile later.

### Finding FX11-04 — CI and Python development dependencies are version ranges/tags

Severity: **Low/Medium build-chain risk**

The Python build system currently specifies `setuptools>=68` and development dependency `pytest>=8`. GitHub Actions uses major-version action tags such as `actions/checkout@v4` and `actions/setup-python@v5`, and the smoke-test container uses the moving `debian:trixie` tag.

This does not directly alter a user's produced ISO unless that CI output is trusted/published, but tighter pinning improves auditability.

**Hardening action:** pin release/build dependencies for reproducible releases and pin CI actions to reviewed commit SHAs for release workflows.

## Required FX11 security rules

Before FX11 is considered release-ready:

1. **No mutable remote code execution.** Never fetch-and-run scripts/config from `main`, `latest`, a paste service or an unverified URL.
2. **No unverified executable downloads.** Third-party executables must come from an approved official source and pass signature/hash verification.
3. **No hidden persistence.** Every service, scheduled task, Run/RunOnce entry, startup item or shell extension created by FX11 must be declared in the manifest and user documentation.
4. **No hidden accounts or credentials.** FX11 must never create an undisclosed local user, embed credentials, SSH keys, tokens or remote-access configuration.
5. **Preserve core security.** Defender, SmartScreen, Windows Update, servicing, activation and recovery are not removed by the standard FX11 profile.
6. **Network transparency.** Windows-side First Run and Control Center should be able to show which vendor/source will be contacted before an optional package is downloaded.
7. **Manifest everything.** Record injected files, hashes, package choices, policies, source ISO hash and builder/tool versions.
8. **Reproducible intent.** A build should be explainable from the selected FX11 profile and manifest without hidden modifications.
9. **Separate recommendations from enforcement.** Security/privacy recommendations remain visible and understandable under `Your System. Your Rules.` except where integrity or destructive-operation safety requires enforcement.
10. **Test in isolation first.** New installer/provisioning behavior must be validated in disposable QEMU/VM environments before physical-machine testing.

## Next audit stages

The initial static review should be followed by:

### Stage 2 — complete code-path audit

- review every FX11 Python function and generated PowerShell/CMD line,
- enumerate all registry keys and Windows servicing actions,
- identify every executable launched,
- enumerate every future network endpoint used by First Run / Control Center,
- verify that no command is constructed unsafely from untrusted input.

### Stage 3 — produced-ISO audit

Build from a known Microsoft ISO in an isolated VM and compare:

- full file inventory against the source ISO,
- added/removed files,
- WIM package/AppX inventory,
- offline registry differences,
- boot.wim changes,
- autounattend/unattend content,
- startup items, services and scheduled tasks,
- firewall rules,
- Defender configuration,
- certificates and trusted roots,
- local users/groups,
- installed drivers.

The goal is to produce a machine-readable **FX11 delta report** showing exactly what changed.

### Stage 4 — runtime network audit

Install FX11 in an isolated VM behind a logging firewall/proxy and observe traffic:

- during Windows Setup,
- first boot/OOBE,
- FX11 First Run,
- idle desktop,
- Control Center package installation.

Unexpected destinations must be investigated before release.

### Stage 5 — integrity/release process

- signed Git tags/releases,
- SHA-256/SHA-512 release checksums,
- optional code signing for Windows-side FX11 binaries/scripts,
- SBOM for FX11 components and build dependencies,
- documented build recipe and tool versions,
- reproducibility checks where practical.

## Current verdict

**No evidence of an intentional backdoor has been found in this initial static review.**

The upstream tiny11 project should nevertheless be treated as an inspiration/reference, not as trusted code to execute or import automatically. FX11 should independently implement reviewed functionality and apply stricter supply-chain and reproducibility rules.

The highest-priority hardening item identified in this pass is to prohibit mutable/unverified build-time downloads and to make the final ISO delta fully auditable.
