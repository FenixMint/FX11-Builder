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
MEDIA_THEME_LOGO_ISO_PATH = f"{MEDIA_THEME_DIR_ISO_PATH}/logo.png"
MEDIA_THEME_FONT_ISO_PATH = f"{MEDIA_THEME_DIR_ISO_PATH}/unicode.pf2"


@dataclass(frozen=True)
class MediaThemePayload:
    theme_config: Path
    background: Path
    logo: Path
    font: Path
    theme_sha256: str
    background_sha256: str
    logo_sha256: str
    font_sha256: str


def default_media_theme() -> str:
    """Return the FX11 installation-media GRUB theme."""
    return "\n".join(
        [
            'title-text: ""',
            'desktop-color: "#07111a"',
            'desktop-image: "background.png"',
            'desktop-image-scale-method: "crop"',
            '',
            '+ image {',
            '  left = 7%',
            '  top = 6%',
            '  width = 30%',
            '  height = 10%',
            '  file = "logo.png"',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 17%',
            '  text = "BOOT. INSTALL. YOUR WAY."',
            '  color = "#8fa8b6"',
            '  font = "Unifont Regular 16"',
            '}',
            '+ boot_menu {',
            '  left = 7%',
            '  top = 29%',
            '  width = 45%',
            '  height = 42%',
            '  item_font = "Unifont Regular 16"',
            '  selected_item_font = "inherit"',
            '  item_color = "#d9e7ee"',
            '  selected_item_color = "#69efa2"',
            '  item_height = 44',
            '  item_padding = 10',
            '  item_spacing = 8',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 74%',
            '  text = "Partition tools powered by GParted"',
            '  color = "#708a97"',
            '  font = "Unifont Regular 16"',
            '}',
            '+ progress_bar {',
            '  id = "__timeout__"',
            '  left = 7%',
            '  top = 81%',
            '  width = 20%',
            '  height = 4',
            '  fg_color = "#69efa2"',
            '  bg_color = "#243640"',
            '}',
            '+ label {',
            '  left = 7%',
            '  top = 89%',
            '  text = "Fenix"',
            '  color = "#7f98a5"',
            '  font = "Unifont Regular 16"',
            '}',
            '+ label {',
            '  left = 61%',
            '  top = 89%',
            '  text = "ENTER  boot     UP/DOWN  select     ESC  back"',
            '  color = "#7f98a5"',
            '  font = "Unifont Regular 16"',
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


def _png_bytes(width: int, height: int, color_type: int, raw: bytes) -> bytes:
    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(raw, 9))
        + _png_chunk(b"IEND", b"")
    )


def _clamp(value: float) -> int:
    return max(0, min(255, int(value)))


def write_media_background(path: Path, *, width: int = 1280, height: int = 720) -> Path:
    """Generate a crop-safe dark landscape with a restrained green aurora."""
    if width < 640 or height < 360:
        raise BuilderError("FX11 media background dimensions are unexpectedly small.")

    horizon = int(height * 0.61)
    mountain_far: list[int] = []
    mountain_near: list[int] = []
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
        far -= height * 0.055 * max(0.0, (xf - 0.48) / 0.52)
        near -= height * 0.080 * max(0.0, (xf - 0.55) / 0.45)
        mountain_far.append(int(far))
        mountain_near.append(int(near))

    raw = bytearray()
    for y in range(height):
        raw.append(0)
        yf = y / max(1, height - 1)
        for x in range(width):
            xf = x / max(1, width - 1)
            side = 0.54 + 0.46 * min(1.0, xf / 0.72)

            if y < horizon:
                sky_t = y / max(1, horizon)
                r = (5 + 6 * sky_t) * side
                g = (14 + 18 * sky_t) * side
                b = (25 + 26 * sky_t) * side

                center = 0.16 + 0.035 * math.sin(xf * 7.0 + 0.7)
                band = math.exp(-((yf - center) / 0.055) ** 2)
                band *= max(0.0, (xf - 0.18) / 0.82)
                g += 64 * band
                b += 35 * band
                r += 7 * band

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

                reflection = math.exp(-((yf - 0.68) / 0.09) ** 2)
                reflection *= max(0.0, (xf - 0.35) / 0.65)
                g += 28 * reflection
                b += 18 * reflection

                ripple = 2.5 * (1.0 + math.sin(y * 0.19 + x * 0.012))
                g += ripple
                b += ripple * 1.4

            raw.extend((_clamp(r), _clamp(g), _clamp(b)))

    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_png_bytes(width, height, 2, bytes(raw)))
    return path


def write_media_logo(path: Path, *, width: int = 520, height: int = 120) -> Path:
    """Generate a transparent geometric FX11 wordmark for the GRUB theme."""
    if width < 320 or height < 80:
        raise BuilderError("FX11 media logo dimensions are unexpectedly small.")

    pixels = bytearray(width * height * 4)

    def set_px(x: int, y: int, rgba: tuple[int, int, int, int]) -> None:
        if 0 <= x < width and 0 <= y < height:
            offset = (y * width + x) * 4
            pixels[offset : offset + 4] = bytes(rgba)

    def rect(x0: int, y0: int, x1: int, y1: int, rgba: tuple[int, int, int, int]) -> None:
        for yy in range(max(0, y0), min(height, y1)):
            for xx in range(max(0, x0), min(width, x1)):
                set_px(xx, yy, rgba)

    def diag(x0: int, y0: int, x1: int, y1: int, thickness: int, rgba: tuple[int, int, int, int]) -> None:
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for step in range(steps + 1):
            t = step / steps
            x = int(x0 + (x1 - x0) * t)
            y = int(y0 + (y1 - y0) * t)
            rect(x - thickness // 2, y - thickness // 2, x + thickness // 2 + 1, y + thickness // 2 + 1, rgba)

    white = (242, 248, 250, 255)
    accent = (105, 239, 162, 255)

    # F
    rect(12, 14, 28, 102, white)
    rect(12, 14, 92, 30, white)
    rect(12, 50, 78, 66, white)

    # X
    diag(115, 16, 190, 100, 14, accent)
    diag(190, 16, 115, 100, 14, accent)

    # 1 1
    for base in (226, 304):
        rect(base + 24, 18, base + 40, 102, white)
        diag(base + 4, 38, base + 28, 18, 12, white)
        rect(base + 4, 88, base + 60, 102, white)

    # Underline / accent rule.
    rect(12, 111, 364, 115, accent)

    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)
        start = y * stride
        raw.extend(pixels[start : start + stride])

    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_png_bytes(width, height, 6, bytes(raw)))
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
    logo = write_media_logo(destination / "logo.png")

    font_source = _find_unicode_font()
    font = destination / "unicode.pf2"
    shutil.copy2(font_source, font)

    return MediaThemePayload(
        theme_config=theme,
        background=background,
        logo=logo,
        font=font,
        theme_sha256=sha256_file(theme),
        background_sha256=sha256_file(background),
        logo_sha256=sha256_file(logo),
        font_sha256=sha256_file(font),
    )
