from fx11.winpe import select_boot_image_index, winpe_update_commands, write_winpe_payload


def test_winpe_payload_runs_wpeinit_before_fx11_launcher(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.startnet.read_text(encoding="ascii")
    assert "wpeinit" in text.lower()
    assert "X:\\FX11\\fx11-launch.cmd" in text


def test_winpeshl_forces_fx11_startnet_as_shell(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.winpeshl.read_text(encoding="ascii")
    assert "[LaunchApps]" in text
    assert "cmd.exe" in text
    assert "startnet.cmd" in text


def test_winpe_launcher_is_non_destructive_bootstrap(tmp_path):
    payload = write_winpe_payload(tmp_path)
    text = payload.launcher.read_text(encoding="ascii")
    assert "FX Partition Manager bootstrap loaded" in text
    assert "diskpart.exe" in text
    assert "clean" not in text.lower()
    assert "format " not in text.lower()
    assert "wpeutil reboot" in text.lower()


def test_boot_wim_declared_boot_index_wins():
    xml = """<WIM><IMAGE INDEX='1'/><IMAGE INDEX='2'/><BOOT INDEX='1'/></WIM>"""
    assert select_boot_image_index(xml) == 1


def test_boot_wim_falls_back_to_setup_index_two():
    xml = """<WIM><IMAGE INDEX='1'/><IMAGE INDEX='2'/></WIM>"""
    assert select_boot_image_index(xml) == 2


def test_winpe_update_plan_replaces_shell_and_adds_fx11_payload(tmp_path):
    payload = write_winpe_payload(tmp_path)
    commands = winpe_update_commands(payload)
    assert "/Windows/System32/startnet.cmd" in commands
    assert "/Windows/System32/winpeshl.ini" in commands
    assert "/FX11/fx11-launch.cmd" in commands
    assert "/FX11/README.txt" in commands
