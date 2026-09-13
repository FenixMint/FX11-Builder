# FX11 Test Hardware

Purpose: persistent hardware validation log for real machines used to prove FX11 behavior beyond VM/synthetic tests.

## Reference target A — HP Laptop 15-db0xxx

Status: planned real-hardware validation target.

User-provided configuration:

- Product family: HP Laptop 15-db0xxx
- Product number: 4UG17EA#AKD
- CPU: AMD A6-9225
- CPU family/architecture: Stoney Ridge / x86-64
- CPU topology: 2 cores / 2 threads
- Clock: 2.6 GHz, boost up to 3.0 GHz
- Cache: 1 MB L2, no L3
- TDP: 15 W
- Integrated GPU: AMD Radeon R4
- RAM: 8 GB DDR4
- Storage: 480 GB SSD in the current configuration
- Display: 15.6 inch, 1920×1080
- Wi-Fi: 802.11ac / Wi-Fi 5
- Ethernet: Gigabit Ethernet
- USB: 2× USB 3.x + 1× USB 2.0
- HDMI: HDMI 1.4b
- Approximate weight: 2.04 kg
- Approximate dimensions: 376 × 246 × 22.5 mm

## Why this machine matters

This machine is intentionally below the class of hardware Microsoft normally positions for supported Windows 11 deployment and is therefore a useful low-end FX11 validation target.

The purpose is not to claim that FX11 can make any obsolete PC fast. The purpose is to verify the project promise:

**FX11 should not block technically possible installation merely because the stock Windows 11 compatibility gate rejects the machine, and the reduced/default FX11 configuration should remain usable on modest hardware where the underlying Windows build can actually boot.**

The AMD A6-9225 is expected to be a severe CPU-side bottleneck compared with modern systems, while 8 GB RAM plus an SSD gives a realistic chance of a usable lightweight desktop if background load is kept under control.

## CPU hard-requirement checkpoint

For current Windows 11 generations, FX11 must distinguish Microsoft policy checks from true CPU instruction requirements.

Before declaring a Windows base image compatible with this target, the real machine must verify CPUID/instruction support required by that Windows build (including newer hard requirements such as POPCNT/SSE4.x where applicable). FX11 may bypass policy/appraiser gates, but it must not pretend to bypass a CPU instruction that the Windows kernel actually executes.

## Planned validation checklist

First real-hardware run should record at least:

- firmware mode and UEFI boot capability,
- Secure Boot state,
- TPM presence/version if any,
- exact CPUID/instruction capabilities,
- FX11 installation-media boot,
- FX Partition Manager disk detection,
- SSD detection and partitioning,
- direct image deployment,
- Windows Boot Manager creation,
- FX Boot Manager installation with Secure Boot OFF for the current development milestone,
- first Windows boot and OOBE,
- Radeon R4 driver status,
- Wi-Fi, Ethernet, audio, USB and HDMI status,
- Windows Update behavior on unsupported hardware,
- Defender/SmartScreen status,
- idle RAM after first stabilization,
- idle CPU activity,
- login-to-desktop time,
- browser launch/responsiveness,
- LibreOffice launch/responsiveness,
- update/reboot cycle,
- sleep/resume and shutdown/restart,
- thermals/fan behavior under ordinary desktop load.

## Performance goal

Do not optimize only for benchmark numbers. On this machine, the main success criteria are perceived usability and low background contention:

- desktop should become responsive quickly after login,
- no permanent high CPU caused by FX11-added services/tasks,
- idle memory should leave meaningful headroom within 8 GB,
- browser and office work should remain practical,
- security/update components preserved by policy should not be disabled merely to manufacture a lower idle number.

## Test policy

Results from this machine should be recorded even when they are bad. FX11 should use the result to tune defaults, not hide limitations.

A weak CPU with SSD is particularly valuable because it exposes background-service and startup regressions that can be invisible on modern CPUs.
