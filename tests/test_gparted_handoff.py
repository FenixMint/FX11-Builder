from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "assets" / "gparted" / "90-fx11-continue"


def test_gparted_handoff_uses_actual_fluxbox_idesk_desktop_model():
    text = HOOK.read_text(encoding="utf-8")

    assert "FX11BOOT" in text
    assert "EFI/FX11/continue-installer" in text
    assert "/root/gparted-live/idesktop" in text
    assert "/home/user/.idesktop" in text
    assert "table Icon" in text
    assert "Caption: FX11 Installer" in text
    assert "Command: /usr/local/bin/fx11-continue" in text
    assert "fluxbox.menu-user" in text
    assert "[exec] (FX11 Installer)" in text


def test_gparted_handoff_keeps_visible_fallback_launcher_and_debug_marker():
    text = HOOK.read_text(encoding="utf-8")

    assert "fx11-installer.desktop" in text
    assert "Continue to FX11 Installer" in text
    assert "/run/fx11-gparted-handoff-ready" in text
