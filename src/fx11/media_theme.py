from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import shutil
import struct
import zlib

from .iso import BuilderError, sha256_file


MEDIA_THEME_DIR_ISO_PATH = "/FX11/media/theme"
MEDIA_THEME_CONFIG_ISO_PATH = f"{MEDIA_THEME_DIR_ISO_PATH}/theme.txt"
MEDIA_THEME_BACKGROUND_ISO_PATH = f"{MEDIA_THEME_DIR_ISO_PATH}/background.png"
MEDIA_THEME_FONT_ISO_PATH = f"{MEDIA_THEME_DIR_ISO_PATH}/unicode.pf2"


@dataclass(frozen=True)
class MediaThemePayload:
    theme_config: Path
    background: Path
    font: Path
    theme_sha256: str
    background_sha256: str
    font_sha256: str


def default_media_theme() -> str:
    """Return the FX11 installation-media GRUB theme.

    The visual direction is deliberately simple enough for firmware GRUB:
    dark landscape background, large FX11 identity, left-side menu and a
    green/teal selection accent. No runtime blur or compositor effects are
    assumed.
    """
    return "\n".join(
        [
            'title-text: ""',
            'desktop-color: "#07111a"',
            'desktop-image: "background.png"',
            'message-color: "#d9e7ee"',
            'message-bg-color: "#07111a"',
            '',
            '+ label {',
            '  left = 7%',
            '  top = 7%',
            '  text = "FX11"',
            '  color = "#f4f8fa"',
            '  font = "Unifont Regular 32"',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 16%',
            '  text = "BOOT. INSTALL. YOUR WAY."',
            '  color = "#8fa8b6"',
            '  font = "Unifont Regular 16"',
            '}',
            '+ boot_menu {',
            '  left = 7%',
            '  top = 29%',
            '  width = 45%',
            '  height = 42%',
            '  item_font = "Unifont Regular 18"',
            '  item_color = "#d9e7ee"',
            '  selected_item_color = "#69efa2"',
            '  item_height = 44',
            '  item_padding = 10',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 74%',
            '  text = "Partition tools powered by GParted"',
            '  color = "#708a97"',
            '  font = "Unifont Regular 14"',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 89%',
            '  text = "Fenix"',
            '  color = "#7f98a5"',
            '  font = "Unifont Regular 14"',
            '}',
            '+ label {',
            '  left = 62%',
            '  top = 89%',
            '  text = "ENTER  boot     UP/DOWN  select     ESC  back"',
            '  color = "#7f98a5"',
            '  font = "Unifont Regular 14"',
            '}',
            '',
        ]
    )


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    )


def _clamp(value: float) -> int:
    return max(0, min(255, int(value)))


def write_media_background(path: Path, *, width: int = 1280, height: int = 720) -> Path:
    """Generate the approved FX11 dark-landscape direction without extra deps."""
    if width < 640 or height < 360:
        raise BuilderError("FX11 media background dimensions are unexpectedly small.")

    horizon = int(height * 0.61)
    mountain_far = []
    mountain_near = []
    for x in range(width):
        xf = x / max(1, width - 1)
        far = height * (
            0.48
            + 0.035 * math.sin(xf * 13.0)
            + 0.020 * math.sin(xf * 31.0 + 1.7)
        )
        near = height * (
            0.535
            + 0.048 * math.sin(xf * 10.0 + 0.4)
            + 0.024 * math.sin(xf * 23.0 + 2.1)
        )
        # Keep the menu side quieter and move the more dramatic ridge right.
        far -= height * 0.055 * max(0.0, (xf - 0.48) / 0.52)
        near -= height * 0.080 * max(0.0, (xf - 0.55) / 0.45)
        mountain_far.append(int(far))
        mountain_near.append(int(near))

    raw = bytearray()
    for y in range(height):
        raw.append(0)  # PNG filter: None
        yf = y / max(1, height - 1)
        for x in range(width):
            xf = x / max(1, width - 1)
            # Keep left side darker for text readability.
            side = 0.54 + 0.46 * min(1.0, xf / 0.72)

            if y < horizon:
                sky_t = y / max(1, horizon)
                r = (5 + 6 * sky_t) * side
                g = (14 + 18 * sky_t) * side
                b = (25 + 26 * sky_t) * side

                # Aurora band: restrained green/teal glow, stronger on the right.
                center = 0.16 + 0.035 * math.sin(xf * 7.0 + 0.7)
                band = math.exp(-((yf - center) / 0.055) ** 2)
                band *= max(0.0, (xf - 0.18) / 0.82)
                g += 64 * band
                b += 35 * band
                r += 7 * band

                # Sparse deterministic stars, mostly outside the menu area.
                if xf > 0.42 and y < int(height * 0.37) and ((x * 71 + y * 37) % 1301 == 0):
                    r, g, b = 165, 189, 198

                if y >= mountain_far[x]:
                    r, g, b = 7, 23, 28
                if y >= mountain_near[x]:
                    r, g, b = 5, 17, 21
            else:
                water_t = (y - horizon) / max(1, height - horizon)
                r = (5 + 3 * (1.0 - water_t)) * side
                g = (19 + 18 * (1.0 - water_t)) * side
                b = (25 + 22 * (1.0 - water_t)) * side

                # Soft horizontal reflection of the aurora/horizon.
                reflection = math.exp(-((yf - 0.68) / 0.09) ** 2)
                reflection *= max(0.0, (xf - 0.35) / 0.65)
                g += 28 * reflection
                b += 18 * reflection

                # Water bands keep the image from looking like a flat gradient.
                ripple = 2.5 * (1.0 + math.sin(y * 0.19 + x * 0.012))
                g += ripple
                b += ripple * 1.4

            raw.extend((_clamp(r), _clamp(g), _clamp(b)))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + _png_chunk(b"IEND", b"")
    )
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def _find_unicode_font() -> Path:
    candidates = (
        Path("/usr/share/grub/unicode.pf2"),
        Path("/usr/share/grub/fonts/unicode.pf2"),
        Path("/usr/share/grub/x86_64-efi/unicode.pf2"),
    )
    for candidate in candidates:
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate
    raise BuilderError(
        "GRUB unicode.pf2 font is required for the FX11 graphical media menu. "
        "Install the grub-common package."
    )


def build_media_theme(destination: Path) -> MediaThemePayload:
    destination = destination.expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)

    theme = destination / "theme.txt"
    theme.write_text(default_media_theme(), encoding="utf-8")

    background = write_media_background(destination / "background.png")

    font_source = _find_unicode_font()
    font = destination / "unicode.pf2"
    shutil.copy2(font_source, font)

    return MediaThemePayload(
        theme_config=theme,
        background=background,
        font=font,
        theme_sha256=sha256_file(theme),
        background_sha256=sha256_file(background),
        font_sha256=sha256_file(font),
    )
