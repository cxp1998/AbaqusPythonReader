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
# Unified App Logo (Matches User Layout Exactly)
# Top-Left: Authentic Abaqus CAE tensile specimen (no white line)
# Bottom-Right: Official Python dual-snake logo
# Top-Right & Bottom-Left: Interactive L-shaped bent arrows
# Transparent background, no blue outer border
# -------------------------------------------------------------
SVG_APP_LOGO = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">
  <defs>
    <!-- Arrow color: Deep teal-blue from user sketch -->
    <linearGradient id="arrowGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b729b"/>
      <stop offset="100%" stop-color="#114e6d"/>
    </linearGradient>

    <!-- Official Python Gradients -->
    <linearGradient id="py_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#387eb8"/>
      <stop offset="100%" stop-color="#2a5f8d"/>
    </linearGradient>
    <linearGradient id="py_yellow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffe052"/>
      <stop offset="100%" stop-color="#f7b318"/>
    </linearGradient>

    <!-- Authentic Abaqus 3D Specimen Gradient -->
    <linearGradient id="abq_grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4e4d8e"/>
      <stop offset="18%" stop-color="#6968aa"/>
      <stop offset="50%" stop-color="#b0ace0"/>
      <stop offset="82%" stop-color="#6968aa"/>
      <stop offset="100%" stop-color="#4e4d8e"/>
    </linearGradient>

    <!-- Abaqus Tensile Specimen (Exact geometry from original CAE icon) -->
    <g id="abaqus_logo">
      <!-- Upper Half -->
      <path fill="url(#abq_grad)"
            d="M 17 0
               H 31
               V 8.73
               A 22 14 0 0 1 46 22
               H 2
               A 22 14 0 0 1 17 8.73
               Z"/>
      <!-- Lower Half (Clean fracture gap between y=22 and y=26) -->
      <path fill="url(#abq_grad)"
            d="M 2 26
               H 46
               A 22 14 0 0 1 31 39.27
               V 48
               H 17
               V 39.27
               A 22 14 0 0 1 2 26
               Z"/>
    </g>

    <!-- Python Official PSF Interlocking Snakes -->
    <g id="python_logo">
      <!-- Blue Snake -->
      <path fill="url(#py_blue)" stroke="#ffffff" stroke-width="2.6" stroke-linejoin="round"
            d="M 55.023 0.2 C 29.052 0.2 28.773 10.281 28.773 12.356 L 28.773 24.95 L 55.523 24.95 L 55.523 28.731 L 18.148 28.731 C 10.199 28.731 0.21 33.564 0.21 54.981 C 0.21 74.654 8.002 82.262 15.866 82.262 L 25.21 82.262 L 25.21 69.137 C 25.21 63.646 27.931 53.481 40.616 53.481 L 67.147 53.481 C 71.049 53.481 82.053 51.785 82.053 39.075 L 82.053 14.856 C 82.053 11.626 81.514 0.2 55.023 0.2 Z"/>
      <!-- Yellow Snake -->
      <path fill="url(#py_yellow)" stroke="#ffffff" stroke-width="2.6" stroke-linejoin="round"
            d="M 55.397 110.2 C 81.356 110.2 81.679 99.929 81.679 98.044 L 81.679 85.45 L 54.897 85.45 L 54.897 81.669 L 92.272 81.669 C 100.281 81.669 110.21 76.715 110.21 55.419 C 110.21 32.097 99.672 28.138 94.554 28.138 L 85.21 28.138 L 85.21 41.263 C 85.21 46.754 82.579 56.919 69.804 56.919 L 43.272 56.919 C 39.38 56.919 28.366 58.815 28.366 71.325 L 28.366 95.544 C 28.366 100.697 31.562 110.2 55.397 110.2 Z"/>
      <!-- Eyes -->
      <circle cx="40.27" cy="13.2" r="4.8" fill="#ffffff"/>
      <circle cx="70.15" cy="96.6" r="4.8" fill="#ffffff"/>
    </g>
  </defs>

  <!-- Top-Left: Abaqus Specimen (Centered at 62, 62) -->
  <g transform="translate(14, 14) scale(2.0)">
    <use href="#abaqus_logo"/>
  </g>

  <!-- Bottom-Right: Python Logo (Centered at 194, 194) -->
  <g transform="translate(145.6, 145.6) scale(0.88)">
    <use href="#python_logo"/>
  </g>

  <!-- Connecting Interactive Dual-Head L-Arrows (180-deg rotational symmetry) -->
  <g fill="url(#arrowGrad)" stroke="#082b3d" stroke-width="2.6" stroke-linejoin="round">
    <!-- Top-Right L-Arrow -->
    <path d="
      M 116 36
      L 140 18
      L 140 26
      L 224 26
      L 224 116
      L 232 116
      L 214 140
      L 196 116
      L 204 116
      L 204 46
      L 140 46
      L 140 54
      Z
    "/>

    <!-- Bottom-Left L-Arrow -->
    <path d="
      M 140 220
      L 116 238
      L 116 230
      L 32 230
      L 32 140
      L 24 140
      L 42 116
      L 60 140
      L 52 140
      L 52 210
      L 116 210
      L 116 202
      Z
    "/>
  </g>
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

