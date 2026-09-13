from hashlib import sha256

from fx11.provisioning import powershell_script, setup_complete_script, write_provisioning_files


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


def test_setup_complete_embeds_expected_ps1_hash():
    expected = "a" * 64
    script = setup_complete_script(expected)
    assert f'set "EXPECTED={expected}"' in script
    assert "Get-FileHash -Algorithm SHA256" in script
    assert "SECURITY ERROR: FX11.ps1 SHA256 mismatch" in script


def test_written_provisioning_hashes_match_files(tmp_path):
    setup, ps1, hashes = write_provisioning_files(tmp_path, ["tiny11-safe", "privacy-balanced"])
    assert sha256(setup.read_bytes()).hexdigest() == hashes["SetupComplete.cmd"]
    assert sha256(ps1.read_bytes()).hexdigest() == hashes["FX11.ps1"]
    setup_text = setup.read_text(encoding="utf-8")
    assert hashes["FX11.ps1"] in setup_text
