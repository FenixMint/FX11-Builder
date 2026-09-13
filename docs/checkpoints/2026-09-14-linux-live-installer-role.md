# Checkpoint — FX11 Installer role inside Linux Live

Date: 2026-09-14

Decision confirmed:

- FX11 Installer is **not** the Microsoft Windows Setup executable and is **not** a Linux distribution installer.
- It is the user-facing FX11 installation application launched inside the FX11 Linux Live environment.
- The Linux Live phase owns language/UX, disk discovery, installation mode selection, guided partitioning, Custom/GParted integration, validation and final confirmation.
- GParted is a subordinate advanced/custom partitioning tool launched from the FX11 Installer and returns control to it after closing.
- For the final Windows deployment, FX11 Installer hands off to WinPE, which remains the trusted Windows-native execution environment for DISM /Apply-Image, BCDBoot, WinRE configuration and related Windows-native tasks.
- The user should experience this as one coherent FX11 installation flow even though the implementation crosses from Linux Live to WinPE internally.

Target user-visible flow:

```text
GRUB
  -> FX11 Linux Live
      -> FX11 Installer
          -> language / mode / disk
          -> partitioning
               -> guided
               -> FX11 + Other OS
               -> Custom -> GParted -> return
          -> validate layout
          -> summary / install
          -> internal handoff to WinPE
              -> DISM /Apply-Image
              -> BCDBoot
              -> WinRE
              -> FX Boot Manager staging/configuration
          -> Windows OOBE
```

UX principle:

The user sees one FX11 Installer. Linux Live and WinPE are implementation layers, not separate products or separate user workflows.
