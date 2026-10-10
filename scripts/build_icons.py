"""Regenerates the static app icon files from SVG_APP_LOGO.

Outputs:
    python_reader/resources/icon_256.png  (README)
    python_reader/app.ico                 (PyInstaller exe / taskbar)

Each ICO size is rendered from the vector source individually rather than
downscaled from 256 px, so small sizes stay crisp.

Usage:
    python scripts/build_icons.py
"""
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image
from PySide6.QtCore import QBuffer, QByteArray, QIODevice, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter
from PySide6.QtSvg import QSvgRenderer

from python_reader.icons import SVG_APP_LOGO

ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]
PNG_PATH = ROOT / "python_reader" / "resources" / "icon_256.png"
ICO_PATH = ROOT / "python_reader" / "app.ico"


def render(renderer: QSvgRenderer, size: int) -> Image.Image:
    img = QImage(size, size, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(p)
    p.end()

    buf = QBuffer()
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    img.save(buf, "PNG")
    return Image.open(io.BytesIO(bytes(buf.data()))).convert("RGBA")


def main():
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)  # noqa: F841
    renderer = QSvgRenderer(QByteArray(SVG_APP_LOGO.encode("utf-8")))
    if not renderer.isValid():
        sys.exit("SVG_APP_LOGO failed to parse")

    images = {s: render(renderer, s) for s in ICO_SIZES}

    images[256].save(PNG_PATH, format="PNG")
    images[256].save(
        ICO_PATH,
        format="ICO",
        sizes=[(s, s) for s in ICO_SIZES],
        append_images=[images[s] for s in ICO_SIZES if s != 256],
    )
    print(f"Wrote {PNG_PATH.relative_to(ROOT)}")
    print(f"Wrote {ICO_PATH.relative_to(ROOT)} ({', '.join(map(str, ICO_SIZES))} px)")


if __name__ == "__main__":
    main()
