from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QIcon, QImage, QPainter, QPixmap
from PySide6.QtCore import Qt, QByteArray

# -------------------------------------------------------------
# Pure Lucide Icon Definitions (24x24 viewBox, 2px stroke, round caps/joins)
# -------------------------------------------------------------

SVG_SUN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="4"/>
  <path d="M12 2v2"/>
  <path d="M12 20v2"/>
  <path d="m4.93 4.93 1.41 1.41"/>
  <path d="m17.66 17.66 1.41 1.41"/>
  <path d="M2 12h2"/>
  <path d="M20 12h2"/>
  <path d="m6.34 17.66-1.41 1.41"/>
  <path d="m19.07 4.93-1.41 1.41"/>
</svg>'''

SVG_MOON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>
</svg>'''

SVG_COPY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="13" height="13" x="9" y="9" rx="2" ry="2"/>
  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
</svg>'''

SVG_CHECK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M20 6 9 17l-5-5"/>
</svg>'''

SVG_FILTER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
</svg>'''

SVG_PIN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="12" y1="17" x2="12" y2="22"/>
  <path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a2 2 0 0 0 0-4H8a2 2 0 0 0 0 4h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"/>
</svg>'''

SVG_MORE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="1.5" fill="{color}"/>
  <circle cx="19" cy="12" r="1.5" fill="{color}"/>
  <circle cx="5" cy="12" r="1.5" fill="{color}"/>
</svg>'''

SVG_CLOSE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M18 6 6 18"/>
  <path d="m6 6 12 12"/>
</svg>'''

SVG_MINUS = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M5 12h14"/>
</svg>'''

SVG_CLEAR = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 6h18"/>
  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
  <line x1="10" x2="10" y1="11" y2="17"/>
  <line x1="14" x2="14" y1="11" y2="17"/>
</svg>'''

SVG_SAVE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
  <polyline points="17 21 17 13 7 13 7 21"/>
  <polyline points="7 3 7 8 15 8"/>
</svg>'''

SVG_FOLDER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2"/>
</svg>'''

SVG_WRAP = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="3" x2="21" y1="6" y2="6"/>
  <path d="M3 12h15a3 3 0 1 1 0 6h-4"/>
  <polyline points="16 16 14 18 16 20"/>
  <line x1="3" x2="10" y1="18" y2="18"/>
</svg>'''

SVG_SCROLL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 17V3"/>
  <path d="m6 11 6 6 6-6"/>
  <path d="M19 21H5"/>
</svg>'''

SVG_HASH = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="4" x2="20" y1="9" y2="9"/>
  <line x1="4" x2="20" y1="15" y2="15"/>
  <line x1="10" x2="8" y1="3" y2="21"/>
  <line x1="16" x2="14" y1="3" y2="21"/>
</svg>'''

SVG_FRAME = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect width="20" height="16" x="2" y="4" rx="2"/>
  <path d="M10 4v4"/>
  <path d="M2 8h20"/>
  <path d="M6 4v4"/>
</svg>'''

SVG_OPACITY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="4" x2="20" y1="21" y2="21"/>
  <line x1="4" x2="20" y1="3" y2="3"/>
  <circle cx="12" cy="12" r="5"/>
  <path d="M12 7v10"/>
</svg>'''

SVG_RESET = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
  <path d="M3 3v5h5"/>
</svg>'''

SVG_INFO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <path d="M12 16v-4"/>
  <path d="M12 8h.01"/>
</svg>'''

SVG_QUIT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
  <polyline points="16 17 21 12 16 7"/>
  <line x1="21" x2="9" y1="12" y2="12"/>
</svg>'''

SVG_CROSSHAIR = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="2" x2="6" y1="12" y2="12"/>
  <line x1="18" x2="22" y1="12" y2="12"/>
  <line x1="12" x2="12" y1="2" y2="6"/>
  <line x1="12" x2="12" y1="18" y2="22"/>
</svg>'''

SVG_LIST_ORDERED = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="10" x2="21" y1="6" y2="6"/>
  <line x1="10" x2="21" y1="12" y2="12"/>
  <line x1="10" x2="21" y1="18" y2="18"/>
  <path d="M4 6h1v4"/>
  <path d="M4 10h2"/>
  <path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"/>
</svg>'''

SVG_ALERT_TRIANGLE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
  <line x1="12" x2="12" y1="9" y2="13"/>
  <line x1="12" x2="12.01" y1="17" y2="17"/>
</svg>'''

SVG_TERMINAL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="4 17 10 11 4 5"/>
  <line x1="12" x2="20" y1="19" y2="19"/>
</svg>'''

SVG_SETTINGS = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/>
  <circle cx="12" cy="12" r="3"/>
</svg>'''

SVG_BOOK_OPEN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
  <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
</svg>'''

SVG_PLAY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polygon points="5 3 19 12 5 21 5 3"/>
</svg>'''

SVG_SHIELD_CHECK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>
  <path d="m9 12 2 2 4-4"/>
</svg>'''


# -------------------------------------------------------------
# Unified App Logo
# Deep indigo rounded tile, original Abaqus CAE glyph as the hero,
# terminal ">_" badge overlapping the lower-right corner.
# Keep in sync with resources/icon.svg; regenerate app.ico and
# icon_256.png with scripts/build_icons.py after editing.
# -------------------------------------------------------------
SVG_APP_LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2f2e6b"/>
      <stop offset="1" stop-color="#0e0c26"/>
    </linearGradient>
    <linearGradient id="abq" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#4e4d8e"/>
      <stop offset=".18" stop-color="#6968aa"/>
      <stop offset=".5" stop-color="#c9c5f2"/>
      <stop offset=".82" stop-color="#6968aa"/>
      <stop offset="1" stop-color="#4e4d8e"/>
    </linearGradient>
    <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".16"/>
      <stop offset=".5" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="badge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#211f52"/>
      <stop offset="1" stop-color="#0c0a22"/>
    </linearGradient>
  </defs>

  <!-- Tile -->
  <rect x="8" y="8" width="240" height="240" rx="56" fill="url(#bg)"/>
  <rect x="8" y="8" width="240" height="240" rx="56" fill="url(#gloss)"/>
  <rect x="8.5" y="8.5" width="239" height="239" rx="55.5" fill="none" stroke="#ffffff" stroke-opacity=".12"/>

  <!-- Original Abaqus CAE glyph (geometry unchanged) -->
  <g transform="translate(40 36) scale(3.1)">
    <path fill="url(#abq)" d="M17 0H31V8.73A22 14 0 0 1 46 22H2A22 14 0 0 1 17 8.73Z"/>
    <path fill="url(#abq)" d="M2 26H46A22 14 0 0 1 31 39.27V48H17V39.27A22 14 0 0 1 2 26Z"/>
  </g>

  <!-- Terminal badge: knockout ring + body + prompt -->
  <rect x="120" y="128" width="120" height="104" rx="30" fill="#13112f"/>
  <rect x="128" y="136" width="104" height="88" rx="22" fill="url(#badge)" stroke="#a5b4fc" stroke-width="5"/>
  <path d="M152 160L172 180L152 200" fill="none" stroke="#a5b4fc" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="182" y="191" width="34" height="11" rx="5.5" fill="#22d3ee"/>
</svg>'''


def render_svg_to_icon(svg_text: str, color="#374151", size=18) -> QIcon:
    """Renders a Lucide SVG string to a crisp multi-size QIcon."""
    formatted_svg = svg_text.format(color=color)
    renderer = QSvgRenderer(QByteArray(formatted_svg.encode("utf-8")))

    icon = QIcon()
    for s in [14, 16, 18, 20, 24, 32, 48]:
        img = QImage(s, s, QImage.Format.Format_ARGB32)
        img.fill(Qt.GlobalColor.transparent)
        p = QPainter(img)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        renderer.render(p)
        p.end()
        icon.addPixmap(QPixmap.fromImage(img))
    return icon


def render_svg_to_pixmap(svg_text: str, color="#374151", size=18) -> QPixmap:
    """Renders a Lucide SVG directly to a single QPixmap at exact pixel size."""
    formatted_svg = svg_text.format(color=color)
    renderer = QSvgRenderer(QByteArray(formatted_svg.encode("utf-8")))
    img = QImage(size, size, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(p)
    p.end()
    return QPixmap.fromImage(img)


def get_app_logo_pixmap(size=20, is_dark=False) -> QPixmap:
    """Returns the unified app logo pixmap featuring Abaqus CAE motif."""
    dpr = 2
    actual_size = size * dpr
    renderer = QSvgRenderer(QByteArray(SVG_APP_LOGO.encode("utf-8")))
    img = QImage(actual_size, actual_size, QImage.Format.Format_ARGB32)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(p)
    p.end()
    pix = QPixmap.fromImage(img)
    pix.setDevicePixelRatio(dpr)
    return pix

