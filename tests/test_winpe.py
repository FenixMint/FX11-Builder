from fx11.winpe import write_winpe_payload


def test_winpe_payload_runs_wpeinit_before_fx11_launcher(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.startnet.read_text(encoding="ascii")
    assert "wpeinit" in text.lower()
    assert "X:\\FX11\\fx11-launch.cmd" in text


def test_winpe_launcher_is_non_destructive_bootstrap(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.launcher.read_text(encoding="ascii")
    assert "FX Partition Manager bootstrap loaded" in text
    assert "diskpart.exe" in text
    assert "clean" not in text.lower()
    assert "format " not in text.lower()
    assert "wpeutil reboot" in text.lower()
