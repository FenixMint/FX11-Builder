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

### Confirmed target notebook: Dell Inspiron 17R N7110

The exact research machine has now been identified as **Dell Inspiron 17R N7110** with Intel graphics plus optional NVIDIA GeForce GT 525M.

Upstream Dell evidence confirms that this model uses NVIDIA Optimus when fitted with the GT 525M. Dell support material for the N7110 includes Windows 7 NVIDIA packages with Optimus support, while Dell community reports describe the Intel GPU as the primary display path and the NVIDIA GPU as the render-offload device.

Important N7110-specific findings:

- Dell shipped N7110 variants with Intel-only graphics and variants with Intel + GeForce GT 525M; the NVIDIA GPU is soldered to the corresponding motherboard and is not an add-in module.
- Dell BIOS history explicitly contains Optimus-related fixes; BIOS A03 fixed a case where the NVIDIA Optimus dGPU disappeared after warm boot.
- Dell currently offers BIOS A13 for the N7110; firmware version should be recorded before experiments and firmware changes must not be performed casually.
- A documented N7110 Windows XP SP3 installation exists where Intel HD graphics worked and the NVIDIA 307.83 XP package was modified to accept the notebook OEM SUBSYS ID. In that reported machine the NVIDIA device used `PCI\VEN_10DE&DEV_0DF5&SUBSYS_04C41028`. This ID is evidence for one N7110 board configuration only; the actual FX test machine must be read from Device Manager/PCI enumeration rather than assumed.
- That INF modification was sufficient to make the GT 525M enumerate in Device Manager, but it did **not** prove working Optimus rendering, Direct3D acceleration, internal-panel output, or GPU switching under XP.
- Dell community reports for the N7110 state that the Intel GPU remains the primary display device and that rendered frames from the NVIDIA GPU normally pass through the Intel path to the internal screen. This is consistent with a muxless Optimus design and makes Windows XP support substantially harder than a simple INF patch.
- There is useful evidence that the N7110 HDMI path depends on the NVIDIA device: one Dell report states that disabling the NVIDIA adapter stopped HDMI picture output while disabling Intel did not. This makes external-HDMI operation an important XP experiment even if the internal LCD cannot use NVIDIA acceleration.

### N7110 XP test plan

The target should be treated as a staged research problem rather than a single driver-install task.

1. Record BIOS version, CPU, RAM and exact motherboard/system identifiers.
2. Boot a known-good Windows 7 installation and record exact Intel/NVIDIA PCI IDs, SUBSYS IDs, ACPI devices, display topology and which GPU owns each physical connector.
3. Update BIOS only if technically justified; preserve the existing version and recovery path first.
4. Build XP Professional SP3 x86 media with the correct Intel AHCI/storage driver integrated so Setup boots natively without IDE fallback.
5. Install Intel chipset and Intel HD Graphics 3000 XP drivers first.
6. Install the official NVIDIA 307.83 XP package unchanged if it matches the exact PCI/SUBSYS ID.
7. If only the OEM SUBSYS match is missing, generate a documented minimal INF patch from the official NVIDIA package and record original package version/hash plus the patch.
8. Validate device state: no Code 10/Code 43, no BSOD, correct clocks/memory detection.
9. Test Direct3D/OpenGL on the NVIDIA device, not merely Device Manager enumeration.
10. Test HDMI output separately with Intel enabled and NVIDIA enabled.
11. Test internal LCD rendering and determine whether any usable render-offload path exists under XP.
12. Only after those steps evaluate deeper approaches such as ACPI/firmware experimentation. BIOS modification is a high-risk last resort and is not part of the normal FX XP path.

### Feasibility classes

**A. Hardware mux or BIOS discrete-only mode exists**

Best case. XP can potentially run the NVIDIA GPU as the active display adapter using an official NVIDIA XP driver, possibly with an INF extension for the notebook SUBSYS ID if the generic package does not match the OEM ID.

**B. Muxless Optimus, internal panel attached to Intel, no discrete-only BIOS option**

Hard case. Standard XP drivers do not provide the Windows 7-era Optimus switching/render-copy stack. Installing both Intel and NVIDIA XP drivers may still fail to provide usable NVIDIA-rendered display output.

An INF modification alone does not solve this architecture problem.

For the Dell N7110, current evidence points strongly toward this class for the internal LCD.

**C. External display output physically attached to NVIDIA**

Potential special case worth testing. If the NVIDIA device can initialize under XP, an externally connected display path may offer a route even when the internal panel is Intel-only. This is hardware-specific and must be verified experimentally.

For the Dell N7110, HDMI is a priority experiment because existing user evidence suggests the HDMI output depends on the NVIDIA adapter.

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
