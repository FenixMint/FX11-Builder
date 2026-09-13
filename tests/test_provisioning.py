from os11vlin.provisioning import powershell_script


def test_tiny11_script_removes_declared_consumer_apps():
    script = powershell_script(["tiny11-safe"])
    assert "Clipchamp.Clipchamp" in script
    assert "Microsoft.XboxGamingOverlay" in script
    assert "Remove-AppxProvisionedPackage" in script


def test_privacy_script_preserves_required_diagnostics():
    script = powershell_script(["privacy-balanced"])
    assert '"AllowTelemetry" 1' in script
    assert '"DisableWindowsConsumerFeatures" 1' in script
    assert '"DisableAIDataAnalysis" 1' in script


def test_tiny11_safe_does_not_target_critical_components():
    script = powershell_script(["tiny11-safe"])
    assert "Microsoft.WindowsStore" not in script
    assert "Windows Defender" not in script
    assert "Microsoft.MicrosoftEdge" not in script
