from fx11.live import LiveMode, calamares_command, calamares_profile, parse_live_mode


def test_parse_fx11_mode_from_kernel_cmdline():
    assert parse_live_mode("quiet splash fx.mode=windows") == LiveMode.FX11
    assert parse_live_mode("fx.mode=fx11") == LiveMode.FX11


def test_parse_fx_linux_mode_from_kernel_cmdline():
    assert parse_live_mode("boot=live fx.mode=linux") == LiveMode.FX_LINUX
    assert parse_live_mode("fx.mode=fxlinux") == LiveMode.FX_LINUX


def test_parse_try_mode():
    assert parse_live_mode("fx.mode=try") == LiveMode.LIVE


def test_missing_or_unknown_mode_is_not_guessed():
    assert parse_live_mode("quiet splash") is None
    assert parse_live_mode("fx.mode=other") is None


def test_calamares_profiles_are_separate():
    assert str(calamares_profile(LiveMode.FX11)).endswith("/fx11")
    assert str(calamares_profile(LiveMode.FX_LINUX)).endswith("/linux")
    assert calamares_profile(LiveMode.LIVE) is None


def test_try_mode_does_not_start_installer():
    assert calamares_command(LiveMode.LIVE) is None


def test_installer_modes_route_to_calamares():
    assert calamares_command(LiveMode.FX11) == (
        "pkexec",
        "calamares",
        "-c",
        "/etc/fx/calamares/fx11",
    )
    assert calamares_command(LiveMode.FX_LINUX) == (
        "pkexec",
        "calamares",
        "-c",
        "/etc/fx/calamares/linux",
    )
