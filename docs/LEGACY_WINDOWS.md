# FX legacy Windows direction

This document records a future compatibility branch for older Microsoft operating systems. It is exploratory and must not be confused with completed FX11 functionality.

## Product idea

After FX11 is working reliably, investigate FX build/install tooling for:

- Windows 7,
- Windows XP,

with the purpose of running older software and hardware that is difficult or impossible to support well on current Windows versions.

Working names such as `FX7` and `FX XP` are provisional only. Product naming is not yet final.

## Legal / distribution boundary

The FX project should follow the same rule used for FX11:

- do not redistribute Microsoft Windows installation binaries as if they were FX-owned software,
- users provide their own appropriately licensed source media,
- the builder modifies/rebuilds user-provided media,
- all FX changes should be declared and reproducible,
- third-party drivers and tools must keep their own licenses/provenance.

## Windows 7 direction

Windows 7 is the easier legacy target and is likely to be useful for:

- older industrial/diagnostic software,
- older games,
- software tied to discontinued drivers or middleware,
- hardware from the late Windows 7 era,
- systems where Windows 10/11 adds unnecessary overhead.

Potential FX work includes:

- driver integration,
- USB 3.x support where appropriate,
- AHCI/NVMe support where technically feasible,
- update/offline-patch strategy,
- modern boot compatibility where practical,
- preserving compatibility instead of over-debloating.

## Windows XP direction

Windows XP is a specialist/legacy target. The likely primary edition for compatibility testing is XP Professional SP3 32-bit, because many older applications and drivers target x86 XP.

The XP project should prioritize:

- AHCI/storage driver integration,
- chipset drivers,
- graphics drivers,
- audio/network drivers,
- ACPI compatibility,
- legacy BIOS/MBR first where required by hardware,
- isolated/offline operation by default because XP is unsupported and unsafe for normal Internet use.

## Specific research target: NVIDIA Optimus + GeForce GT 525M + Intel iGPU

A key user target is a Sandy Bridge-era notebook with:

- NVIDIA GeForce GT 525M,
- Intel integrated graphics (commonly Intel HD Graphics 3000 on this platform),
- NVIDIA Optimus / hybrid graphics topology.

Important findings:

1. NVIDIA published Windows XP notebook drivers that list the GeForce GT 525M as supported hardware (for example the 307.83 XP driver family).
2. Intel published Windows XP drivers for Intel HD Graphics 3000.
3. NVIDIA's own Optimus documentation states that Optimus requires Windows 7 or later.

Therefore the central problem is **not merely finding an XP driver for each GPU**. The difficult part is the hybrid/muxless Optimus presentation path and GPU switching.

### What must be determined for the exact laptop

Before deciding whether full NVIDIA acceleration under XP is achievable, identify:

- exact notebook manufacturer/model,
- BIOS version,
- CPU and exact Intel GPU,
- NVIDIA PCI device ID and SUBSYS ID,
- Intel PCI device ID and SUBSYS ID,
- whether the internal panel is physically wired only to the Intel GPU,
- whether HDMI/DisplayPort is wired to NVIDIA or Intel,
- whether the machine contains a hardware display mux,
- whether BIOS offers `Integrated`, `Discrete`, `Switchable`, `Optimus`, or similar graphics modes.

### Feasibility classes

**A. Hardware mux or BIOS discrete-only mode exists**

Best case. XP can potentially run the NVIDIA GPU as the active display adapter using an official NVIDIA XP driver, possibly with an INF extension for the notebook SUBSYS ID if the generic package does not match the OEM ID.

**B. Muxless Optimus, internal panel attached to Intel, no discrete-only BIOS option**

Hard case. Standard XP drivers do not provide the Windows 7-era Optimus switching/render-copy stack. Installing both Intel and NVIDIA XP drivers may still fail to provide usable NVIDIA-rendered display output.

An INF modification alone does not solve this architecture problem.

**C. External display output physically attached to NVIDIA**

Potential special case worth testing. If the NVIDIA device can initialize under XP, an externally connected display path may offer a route even when the internal panel is Intel-only. This is hardware-specific and must be verified experimentally.

### Research policy

Start only from trustworthy driver sources:

- NVIDIA official archived packages,
- Intel official archived packages,
- notebook OEM packages where available.

If an OEM SUBSYS ID is missing from an official NVIDIA XP INF, FX may generate a documented INF patch from the official package rather than immediately rely on opaque third-party repacks.

Any modified/unsigned driver must be clearly marked as modified and must retain its original source/version/hash information.

### Success levels for the GT 525M target

The project should distinguish:

1. device enumerates,
2. driver loads without Code 10/Code 43/BSOD,
3. NVIDIA control panel/driver reports the GPU correctly,
4. external output works (if NVIDIA-wired),
5. Direct3D/OpenGL acceleration works,
6. internal LCD can display NVIDIA-rendered applications,
7. automatic or manual GPU switching works.

Do not call the Optimus target solved merely because Device Manager shows the GT 525M.

## Security position for XP

XP must be treated as a legacy application environment, not a general-purpose Internet workstation.

Recommended product stance:

- offline by default,
- network enablement explicit,
- clear unsupported/EOL warning,
- no claim of modern security,
- encourage file transfer through controlled means or isolated networks/VMs.

## Relationship to FX11

FX11 remains the current priority. Legacy Windows work begins only after the main FX11 install/build path is stable enough that it does not distract from the first release milestone.
