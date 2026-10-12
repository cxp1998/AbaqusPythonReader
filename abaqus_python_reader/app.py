import os
import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMenu, QFileDialog, QMessageBox,
    QSystemTrayIcon, QFrame, QApplication
)
from PySide6.QtGui import (
    QIcon, QFont, QCursor, QColor, QPixmap, QPainter, QImage, QAction
)
from PySide6.QtCore import (
    Qt, QPoint, QRect, QSize, QTimer, QByteArray
)
from PySide6.QtSvg import QSvgRenderer

from . import __version__
from .config import ConfigManager
from .file_monitor import FileMonitor
from .cleaner import clean_abaqus_script, has_mask_statement
from .editor import CodeEditor
from .highlighter import THEMES
from .icons import (
    render_svg_to_icon, render_svg_to_pixmap, get_app_logo_pixmap,
    SVG_APP_LOGO,
    SVG_SUN, SVG_MOON, SVG_COPY, SVG_CHECK, SVG_PIN, SVG_FILTER,
    SVG_MORE, SVG_MINUS, SVG_CLOSE, SVG_CLEAR, SVG_SAVE, SVG_FOLDER,
    SVG_WRAP, SVG_SCROLL, SVG_HASH, SVG_FRAME, SVG_OPACITY,
    SVG_RESET, SVG_INFO, SVG_QUIT,
    SVG_CROSSHAIR, SVG_LIST_ORDERED, SVG_ALERT_TRIANGLE,
    SVG_SETTINGS, SVG_BOOK_OPEN, SVG_TERMINAL, SVG_GLOBE
)
from .abaqus_mode import (
    MODE_COORDINATE, MODE_INDEX, MODE_COMPRESSED,
    get_mode_info,
    AbaqusModeDialog, AbaqusGuideDialog,
    find_abaqus_window, activate_abaqus_window
)
from .i18n import tr, set_language, get_language, SUPPORTED_LANGUAGES


RESOURCES_DIR = Path(__file__).resolve().parent / "resources"
SVG_ICON_PATH = str(RESOURCES_DIR / "icon.svg")
ICO_ICON_PATH = str(Path(__file__).resolve().parent / "app.ico")


def get_vector_icon(size=32) -> QIcon:
    """Renders scalable vector SVG icon into crisp multi-resolution QIcon."""
    icon = QIcon()
    renderer = None
    if SVG_APP_LOGO:
        renderer = QSvgRenderer(QByteArray(SVG_APP_LOGO.encode("utf-8")))
    elif os.path.exists(SVG_ICON_PATH):
        renderer = QSvgRenderer(SVG_ICON_PATH)

    if renderer and renderer.isValid():
        for s in [16, 20, 24, 32, 40, 48, 64, 128, 256]:
            img = QImage(s, s, QImage.Format.Format_ARGB32)
            img.fill(Qt.GlobalColor.transparent)
            p = QPainter(img)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            renderer.render(p)
            p.end()
            icon.addPixmap(QPixmap.fromImage(img))
        return icon
    elif os.path.exists(ICO_ICON_PATH):
        return QIcon(ICO_ICON_PATH)
    return QIcon()


class ToastOverlay(QLabel):
    """Floating HUD pill notification for clear, immediate feedback on settings changes."""
    def __init__(self, parent):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 9, QFont.Weight.Medium))
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.hide()
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_message(self, text: str, is_active: bool = True, duration_ms: int = 1500):
        is_dark = self.parent().config.get("dark_theme", False)
        if is_dark:
            bg = "rgba(15, 23, 42, 0.94)"
            border = "#38bdf8" if is_active else "#475569"
            fg = "#38bdf8" if is_active else "#94a3b8"
        else:
            bg = "rgba(255, 255, 255, 0.96)"
            border = "#0284c7" if is_active else "#94a3b8"
            fg = "#0284c7" if is_active else "#475569"

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg};
                border: 1px solid {border};
                border-radius: 14px;
                padding: 4px 16px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        self.setText(text)
        self.adjustSize()
        self.setFixedHeight(28)

        # Center horizontally, 14px above bottom
        pw = self.parent().width()
        ph = self.parent().height()
        w = max(self.width() + 10, 120)
        self.resize(w, 28)
        self.move((pw - w) // 2, ph - 42)

        self.show()
        self.raise_()
        self._timer.start(duration_ms)


class ToggleMenu(QMenu):
    """QMenu that marks "on" toggle actions with a right-aligned Lucide check icon.

    Checkable QActions are avoided because Qt's Windows styles replace the action's
    icon with the check mark; here the function icon stays on the left.
    """
    CHECK_SIZE = 15
    CHECK_MARGIN = 10

    def __init__(self, parent=None, check_color="#475569"):
        super().__init__(parent)
        self.setObjectName("ToggleMenu")
        # Same stroke weight as other menu icons (SVG_CHECK is drawn bolder for buttons)
        check_svg = SVG_CHECK.replace('stroke-width="2.5"', 'stroke-width="2"')
        self._check_icon = render_svg_to_icon(check_svg, color=check_color, size=self.CHECK_SIZE)

    def add_toggle(self, icon: QIcon, text: str, is_on: bool, slot) -> QAction:
        act = self.addAction(icon, text, slot)
        act.setProperty("toggle_on", is_on)
        return act

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        s = self.CHECK_SIZE
        for act in self.actions():
            if act.property("toggle_on"):
                r = self.actionGeometry(act)
                self._check_icon.paint(painter, QRect(r.right() - self.CHECK_MARGIN - s, r.center().y() - s // 2, s, s))
        painter.end()


class MainWindow(QMainWindow):
    RESIZE_MARGIN = 6

    def __init__(self):
        super().__init__()
        self.config = ConfigManager()

        # Initialize language configuration
        current_lang = self.config.get("language", "en")
        set_language(current_lang)

        self.toast = None
        self.file_monitor = FileMonitor()

        # State tracking
        self.raw_text_buffer = ""
        self._right_drag_active = False
        self._right_click_pos = QPoint()
        self._window_start_pos = QPoint()
        self._app_icon = get_vector_icon()

        self._init_ui()
        self._init_tray()
        self._connect_signals()

        # Load file & start monitoring
        last_file = self.config.get("last_file", "abaqus.rpy")
        self.file_monitor.set_file(last_file)
        self.file_monitor.start()

    def show_toast(self, text: str, is_active: bool = True, duration_ms: int = 1500):
        if not hasattr(self, "toast") or self.toast is None:
            self.toast = ToastOverlay(self)
        self.toast.show_message(text, is_active=is_active, duration_ms=duration_ms)

    def _init_ui(self):
        self.setWindowIcon(self._app_icon)
        self.setWindowTitle("AbaqusPythonReader")

        # Geometry
        x = self.config.get("window_x", 200)
        y = self.config.get("window_y", 150)
        w = self.config.get("window_width", 760)
        h = self.config.get("window_height", 320)
        self.setGeometry(x, y, w, h)

        # Flags & Opacity
        self._update_window_flags()
        opacity_val = self.config.get("opacity", 95) / 100.0
        self.setWindowOpacity(opacity_val)

        # Central Widget
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        # Top Bar
        self.top_bar = self._create_top_bar()
        layout.addWidget(self.top_bar)

        # Code Editor
        theme = "dark" if self.config.get("dark_theme", False) else "light"
        show_lines = self.config.get("show_line_numbers", True)
        self.editor = CodeEditor(self, theme_name=theme, show_line_numbers=show_lines)
        self.editor.auto_scroll = self.config.get("auto_scroll", True)
        self.editor.setLineWrapMode(
            CodeEditor.LineWrapMode.WidgetWidth if self.config.get("word_wrap", True)
            else CodeEditor.LineWrapMode.NoWrap
        )
        layout.addWidget(self.editor)

        self.setMouseTracking(True)
        self.central_widget.setMouseTracking(True)
        self._apply_theme_style()

    def _create_top_bar(self):
        bar = QWidget()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(34)

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(6)

        # Unified Logo Icon
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(18, 18)
        self.lbl_logo.setScaledContents(True)
        layout.addWidget(self.lbl_logo)

        # App Title
        self.lbl_title = QLabel("AbaqusPythonReader")
        self.lbl_title.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        layout.addWidget(self.lbl_title)

        # File Badge Button (Clean pill: status dot + file name)
        self.btn_file = QPushButton("● abaqus.rpy")
        self.btn_file.setObjectName("FileBadge")
        self.btn_file.setToolTip(tr("btn_file_tooltip"))
        self.btn_file.clicked.connect(self._browse_file)
        layout.addWidget(self.btn_file)

        # Mask Warning Badge (Shown when getSequenceFromMask is detected)
        self.btn_mask_warning = QPushButton(tr("btn_mask_warning"))
        self.btn_mask_warning.setObjectName("MaskWarning")
        self.btn_mask_warning.setToolTip(tr("btn_mask_warning_tooltip"))
        self.btn_mask_warning.clicked.connect(self._show_abaqus_mode_dialog)
        self.btn_mask_warning.hide()
        layout.addWidget(self.btn_mask_warning)

        layout.addStretch()

        # 1. Viewport filter toggle
        self.btn_filter = QPushButton(tr("btn_filter"))
        self.btn_filter.setCheckable(True)
        self.btn_filter.setChecked(self.config.get("filter_viewport", True))
        self.btn_filter.setToolTip(tr("btn_filter_tooltip"))
        self.btn_filter.clicked.connect(self._toggle_filter)
        self.btn_filter.toggled.connect(self._update_button_icons)
        layout.addWidget(self.btn_filter)

        # 2. Copy cleaned code
        self.btn_copy = QPushButton(tr("btn_copy"))
        self.btn_copy.setToolTip(tr("btn_copy_tooltip"))
        self.btn_copy.clicked.connect(self._copy_clean_code)
        layout.addWidget(self.btn_copy)

        # 3. Always on top
        self.btn_pin = QPushButton()
        self.btn_pin.setCheckable(True)
        self.btn_pin.setFixedWidth(28)
        self.btn_pin.setChecked(self.config.get("topmost", True))
        self.btn_pin.setToolTip(tr("btn_pin_tooltip"))
        self.btn_pin.clicked.connect(self._toggle_topmost)
        self.btn_pin.toggled.connect(self._update_button_icons)
        layout.addWidget(self.btn_pin)

        # 4. Theme switch (Lucide Vector Sun / Moon)
        self.btn_theme = QPushButton()
        self.btn_theme.setFixedWidth(28)
        self.btn_theme.setToolTip(tr("btn_theme_tooltip"))
        self.btn_theme.clicked.connect(self._toggle_theme)
        layout.addWidget(self.btn_theme)

        # 5. More menu (Lucide Horizontal More)
        self.btn_more = QPushButton()
        self.btn_more.setFixedWidth(28)
        self.btn_more.setToolTip(tr("btn_more_tooltip"))
        self.btn_more.clicked.connect(self._show_more_menu)
        layout.addWidget(self.btn_more)

        # 6. Minimize to taskbar (Lucide Minus)
        self.btn_minimize = QPushButton()
        self.btn_minimize.setFixedWidth(26)
        self.btn_minimize.setToolTip(tr("btn_minimize_tooltip"))
        self.btn_minimize.clicked.connect(self.showMinimized)
        layout.addWidget(self.btn_minimize)

        # 7. Close button (Lucide Close X)
        self.btn_close = QPushButton()
        self.btn_close.setFixedWidth(26)
        self.btn_close.setObjectName("CloseBtn")
        self.btn_close.setToolTip(tr("btn_close_tooltip"))
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)

        return bar

    def _retranslate_ui(self):
        """Refreshes all user-visible strings across UI elements and menus."""
        self.btn_file.setToolTip(tr("btn_file_tooltip"))
        self.btn_mask_warning.setText(tr("btn_mask_warning"))
        self.btn_mask_warning.setToolTip(tr("btn_mask_warning_tooltip"))
        self.btn_filter.setText(tr("btn_filter"))
        self.btn_filter.setToolTip(tr("btn_filter_tooltip"))
        self.btn_copy.setText(tr("btn_copy"))
        self.btn_copy.setToolTip(tr("btn_copy_tooltip"))
        self.btn_pin.setToolTip(tr("btn_pin_tooltip"))
        self.btn_theme.setToolTip(tr("btn_theme_tooltip"))
        self.btn_more.setToolTip(tr("btn_more_tooltip"))
        self.btn_minimize.setToolTip(tr("btn_minimize_tooltip"))
        self.btn_close.setToolTip(tr("btn_close_tooltip"))

        # Re-initialize tray menu with translated items
        self._init_tray()

        # Re-evaluate file status label
        self.file_monitor.refresh_status()

    def _set_language(self, lang_code: str):
        """Switches UI language between English and Chinese and saves to configuration."""
        self.config.set("language", lang_code)
        set_language(lang_code)
        self._retranslate_ui()
        self.show_toast(tr("toast_lang_changed"), is_active=True)

    def _update_button_icons(self):
        """Updates all Lucide vector icons based on current theme and checked state."""
        is_dark = self.config.get("dark_theme", False)
        icon_color = "#cbd5e1" if is_dark else "#475569"

        # Unified App Logo
        self.lbl_logo.setPixmap(get_app_logo_pixmap(size=18, is_dark=is_dark))

        # Mask Warning Button
        self.btn_mask_warning.setIcon(render_svg_to_icon(SVG_ALERT_TRIANGLE, color="#f59e0b" if is_dark else "#d97706", size=13))

        # Filter Button: white icon if checked (active blue bg), else normal icon_color
        filter_color = "#ffffff" if self.btn_filter.isChecked() else icon_color
        self.btn_filter.setIcon(render_svg_to_icon(SVG_FILTER, color=filter_color, size=13))

        # Copy Button: normal icon_color
        self.btn_copy.setIcon(render_svg_to_icon(SVG_COPY, color=icon_color, size=13))

        # Pin Button: white icon if checked (active blue bg), else normal icon_color
        pin_color = "#ffffff" if self.btn_pin.isChecked() else icon_color
        self.btn_pin.setIcon(render_svg_to_icon(SVG_PIN, color=pin_color, size=14))

        # Theme Icon: If currently dark, show Sun; if light, show Moon
        theme_svg = SVG_SUN if is_dark else SVG_MOON
        theme_color = "#f59e0b" if is_dark else "#6366f1"
        self.btn_theme.setIcon(render_svg_to_icon(theme_svg, color=theme_color, size=15))

        # More, Minimize and Close
        self.btn_more.setIcon(render_svg_to_icon(SVG_MORE, color=icon_color, size=14))
        self.btn_minimize.setIcon(render_svg_to_icon(SVG_MINUS, color=icon_color, size=12))
        self.btn_close.setIcon(render_svg_to_icon(SVG_CLOSE, color=icon_color, size=12))

    def _update_window_flags(self):
        flags = Qt.WindowType.Window
        if self.config.get("frameless", True):
            # Minimize hint keeps WS_MINIMIZEBOX so the taskbar button can still minimize/restore
            flags |= Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowMinimizeButtonHint
        if self.config.get("topmost", True):
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _connect_signals(self):
        self.file_monitor.new_content_appended.connect(self._on_new_content)
        self.file_monitor.file_reset.connect(self._on_file_reset)
        self.file_monitor.file_status_changed.connect(self._on_file_status_changed)

    def _on_new_content(self, chunk: str):
        self.raw_text_buffer += chunk
        self._refresh_editor_content()

    def _on_file_reset(self):
        self.raw_text_buffer = ""
        self.btn_mask_warning.hide()
        self.editor.clear()

    def _on_file_status_changed(self, is_active: bool, msg: str):
        filename = os.path.basename(self.file_monitor.filepath) if self.file_monitor.filepath else tr("no_file_selected")
        if is_active:
            self.btn_file.setText(f"● {filename}")
            self.btn_file.setStyleSheet("color: #059669; font-weight: 600;")
        else:
            self.btn_file.setText(f"○ {filename}")
            self.btn_file.setStyleSheet("color: #d97706; font-weight: 600;")

        self.btn_file.setToolTip(f"{msg}\n{self.file_monitor.filepath}")

    def _refresh_editor_content(self):
        filter_active = self.config.get("filter_viewport", True)
        processed_text = clean_abaqus_script(self.raw_text_buffer, filter_viewport=filter_active)

        # Smart inspection: check if getSequenceFromMask exists in raw text
        has_mask = has_mask_statement(self.raw_text_buffer)
        self.btn_mask_warning.setVisible(has_mask)

        vbar = self.editor.verticalScrollBar()
        old_val = vbar.value()
        is_at_bottom = old_val >= vbar.maximum() - 20

        self.editor.setPlainText(processed_text)

        if self.config.get("auto_scroll", True) or is_at_bottom:
            self.editor.scroll_to_bottom()
        else:
            vbar.setValue(old_val)

    def _toggle_filter(self):
        new_val = self.btn_filter.isChecked()
        self.config.set("filter_viewport", new_val)
        self._refresh_editor_content()
        self._update_button_icons()
        self.show_toast(tr("toast_filter_hidden") if new_val else tr("toast_filter_shown"), is_active=new_val)

    def _copy_clean_code(self):
        text = clean_abaqus_script(self.raw_text_buffer, filter_viewport=True)
        if not text.strip():
            text = self.editor.toPlainText()
        QApplication.clipboard().setText(text)

        # Temporary button feedback with Lucide check icon
        self.btn_copy.setText(tr("btn_copy_done"))
        self.btn_copy.setIcon(render_svg_to_icon(SVG_CHECK, color="#10b981", size=13))
        QTimer.singleShot(1200, self._restore_copy_button)

    def _restore_copy_button(self):
        is_dark = self.config.get("dark_theme", False)
        icon_color = "#cbd5e1" if is_dark else "#475569"
        self.btn_copy.setText(tr("btn_copy"))
        self.btn_copy.setIcon(render_svg_to_icon(SVG_COPY, color=icon_color, size=13))

    def _clear_view(self):
        self.raw_text_buffer = ""
        self.btn_mask_warning.hide()
        self.editor.clear()
        self.show_toast(tr("toast_cleared"), is_active=False)

    def _toggle_topmost(self):
        new_val = self.btn_pin.isChecked()
        self.config.set("topmost", new_val)
        self._update_window_flags()
        self.show()
        self._update_button_icons()
        self.show_toast(tr("toast_pinned") if new_val else tr("toast_unpinned"), is_active=new_val)

    def _toggle_theme(self):
        is_dark = not self.config.get("dark_theme", False)
        self.config.set("dark_theme", is_dark)
        theme_name = "dark" if is_dark else "light"
        self.editor.apply_theme(theme_name)
        self._apply_theme_style()

    def _browse_file(self):
        initial_dir = os.path.dirname(self.file_monitor.filepath) if self.file_monitor.filepath else os.getcwd()
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            tr("dlg_open_title"),
            initial_dir,
            tr("dlg_open_filter")
        )
        if filepath:
            self.config.set("last_file", filepath)
            self.file_monitor.set_file(filepath)

    def _save_as_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            tr("dlg_save_title"),
            os.getcwd(),
            tr("dlg_save_filter")
        )
        if filepath:
            text = clean_abaqus_script(self.raw_text_buffer, filter_viewport=True)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                self.show_toast(tr("toast_saved", filename=os.path.basename(filepath)), is_active=True)
            except Exception as e:
                QMessageBox.critical(self, tr("dlg_save_failed_title"), str(e))

    def _build_menu(self, context: bool = False) -> QMenu:
        """Builds the main menu shared by the "more" button and the right-click context menu."""
        is_dark = self.config.get("dark_theme", False)
        action_color = "#94a3b8" if is_dark else "#475569"

        def icon(svg):
            return render_svg_to_icon(svg, color=action_color, size=15)

        menu = ToggleMenu(self, check_color=action_color)

        if context:
            menu.addAction(icon(SVG_COPY), tr("menu_copy"), self._copy_clean_code)
        menu.addAction(icon(SVG_CLEAR), tr("menu_clear"), self._clear_view)
        menu.addAction(icon(SVG_FOLDER), tr("menu_open_file"), self._browse_file)
        menu.addAction(icon(SVG_SAVE), tr("menu_save_as"), self._save_as_file)
        menu.addSeparator()

        if context:
            menu.add_toggle(icon(SVG_FILTER), tr("menu_hide_viewport"), self.btn_filter.isChecked(), lambda: self.btn_filter.click())
        menu.add_toggle(icon(SVG_WRAP), tr("menu_word_wrap"), self.config.get("word_wrap", True), lambda: self._toggle_word_wrap())
        menu.add_toggle(icon(SVG_SCROLL), tr("menu_auto_scroll"), self.config.get("auto_scroll", True), lambda: self._toggle_auto_scroll())
        menu.add_toggle(icon(SVG_HASH), tr("menu_line_numbers"), self.config.get("show_line_numbers", True), lambda: self._toggle_line_numbers())
        menu.add_toggle(icon(SVG_FRAME), tr("menu_frameless"), self.config.get("frameless", True), lambda: self._toggle_frameless())

        # Opacity submenu
        current_op = self.config.get("opacity", 95)
        opacity_menu = ToggleMenu(menu, check_color=action_color)
        opacity_menu.setTitle(tr("menu_opacity"))
        opacity_menu.setIcon(icon(SVG_OPACITY))
        for val in [100, 95, 90, 80, 70, 60, 50]:
            opacity_menu.add_toggle(QIcon(), f"{val}%", val == current_op, lambda v=val: self._set_opacity(v))
        menu.addMenu(opacity_menu)

        # Language selection submenu
        lang_menu = ToggleMenu(menu, check_color=action_color)
        lang_menu.setTitle(tr("menu_language"))
        lang_menu.setIcon(icon(SVG_GLOBE))
        current_lang = get_language()
        for lang_code, lang_name in SUPPORTED_LANGUAGES.items():
            lang_menu.add_toggle(
                QIcon(),
                lang_name,
                lang_code == current_lang,
                lambda lc=lang_code: self._set_language(lc)
            )
        menu.addMenu(lang_menu)

        menu.addSeparator()
        menu.addMenu(self._build_mode_menu(menu, action_color))
        menu.addSeparator()
        menu.addAction(icon(SVG_RESET), tr("menu_reset_window"), self._reset_window_geometry)
        menu.addAction(icon(SVG_INFO), tr("menu_about"), self._show_about)

        if context:
            menu.addSeparator()
            menu.addAction(icon(SVG_QUIT), tr("menu_quit"), self.close)

        return menu

    def _show_more_menu(self):
        menu = self._build_menu()
        self.btn_more.setChecked(True)
        menu.exec(self.btn_more.mapToGlobal(QPoint(0, self.btn_more.height() + 2)))
        self.btn_more.setChecked(False)

    def _toggle_word_wrap(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("word_wrap", True)
        self.config.set("word_wrap", checked)
        self.editor.setLineWrapMode(
            CodeEditor.LineWrapMode.WidgetWidth if checked else CodeEditor.LineWrapMode.NoWrap
        )
        status = tr("state_on") if checked else tr("state_off")
        self.show_toast(tr("toast_word_wrap", state=status), is_active=checked)

    def _toggle_auto_scroll(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("auto_scroll", True)
        self.config.set("auto_scroll", checked)
        self.editor.auto_scroll = checked
        if checked:
            self.editor.scroll_to_bottom()
        status = tr("state_on") if checked else tr("state_off")
        self.show_toast(tr("toast_auto_scroll", state=status), is_active=checked)

    def _toggle_line_numbers(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("show_line_numbers", True)
        self.config.set("show_line_numbers", checked)
        self.editor.set_line_numbers_visible(checked)
        status = tr("state_on") if checked else tr("state_off")
        self.show_toast(tr("toast_line_numbers", state=status), is_active=checked)

    def _toggle_frameless(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("frameless", True)
        self.config.set("frameless", checked)
        self._update_window_flags()
        self.show()
        status = tr("state_on") if checked else tr("state_off")
        self.show_toast(tr("toast_frameless", state=status), is_active=checked)

    def _set_opacity(self, percent: int):
        self.config.set("opacity", percent)
        self.setWindowOpacity(percent / 100.0)
        self.show_toast(tr("toast_opacity", percent=percent), is_active=True)

    def _reset_window_geometry(self):
        screen = QApplication.primaryScreen().geometry()
        w, h = 760, 320
        x = (screen.width() - w) // 2
        y = (screen.height() - h) // 2
        self.setGeometry(x, y, w, h)
        self.config.set("window_x", x)
        self.config.set("window_y", y)
        self.config.set("window_width", w)
        self.config.set("window_height", h)
        self.show_toast(tr("toast_window_centered"), is_active=True)

    def _show_about(self):
        QMessageBox.about(
            self,
            tr("about_title"),
            f"<h3>AbaqusPythonReader {__version__}</h3>"
            f"<p>{tr('about_desc')}</p>"
            f"<p>{tr('about_author')}</p>"
            f"<p>{tr('about_license')}</p>"
        )

    def _build_mode_menu(self, parent: QMenu, action_color: str) -> QMenu:
        """Recording-mode submenu: copy a journalOptions command for the running Abaqus session."""
        menu = QMenu(tr("menu_recording_mode"), parent)
        menu.setIcon(render_svg_to_icon(SVG_CROSSHAIR, color=action_color, size=15))
        for mode_key, svg, color in [
            (MODE_COORDINATE, SVG_CROSSHAIR, "#10b981"),
            (MODE_INDEX, SVG_LIST_ORDERED, "#3b82f6"),
            (MODE_COMPRESSED, SVG_TERMINAL, action_color),
        ]:
            info = get_mode_info(mode_key)
            act = menu.addAction(
                render_svg_to_icon(svg, color=color, size=15),
                info["title"],
                lambda m=mode_key: self._quick_set_mode(m)
            )
            act.setToolTip(tr("mode_tooltip_cmd", cmd=info["command"]))
        menu.setToolTipsVisible(True)
        menu.addSeparator()
        menu.addAction(
            render_svg_to_icon(SVG_SETTINGS, color=action_color, size=15),
            tr("mode_set_default"),
            self._show_abaqus_mode_dialog
        )
        menu.addAction(
            render_svg_to_icon(SVG_BOOK_OPEN, color=action_color, size=15),
            tr("mode_guide"),
            self._show_guide_dialog
        )
        return menu

    def _quick_set_mode(self, mode_key: str):
        info = get_mode_info(mode_key)
        QApplication.clipboard().setText(info["command"])

        hwnd = find_abaqus_window()
        if hwnd:
            activate_abaqus_window(hwnd)

        self.show_toast(tr("mode_copied_toast", badge=info["badge"]), is_active=True, duration_ms=3000)

    def _show_abaqus_mode_dialog(self):
        dlg = AbaqusModeDialog(self, is_dark=self.config.get("dark_theme", False))
        dlg.exec()

    def _show_guide_dialog(self):
        dlg = AbaqusGuideDialog(self, is_dark=self.config.get("dark_theme", False))
        dlg.exec()

    def _apply_theme_style(self):
        is_dark = self.config.get("dark_theme", False)
        colors = THEMES["dark" if is_dark else "light"]

        if is_dark:
            badge_bg = "rgba(137, 180, 250, 0.12)"
            badge_border = "rgba(137, 180, 250, 0.25)"
            active_btn_bg = "#3b82f6"
            active_btn_fg = "#ffffff"
            warn_bg = "rgba(245, 158, 11, 0.18)"
            warn_border = "rgba(245, 158, 11, 0.4)"
            warn_fg = "#fbbf24"
        else:
            badge_bg = "#f3f4f6"
            badge_border = "#e5e7eb"
            active_btn_bg = "#2563eb"
            active_btn_fg = "#ffffff"
            warn_bg = "#fef3c7"
            warn_border = "#fde68a"
            warn_fg = "#b45309"

        self.setStyleSheet(f"""
            QWidget#CentralWidget {{
                background-color: {colors["background"]};
                border: 1px solid {colors["border"]};
                border-radius: 6px;
            }}
            QWidget#TopBar {{
                background-color: {colors["toolbar_bg"]};
                border-bottom: 1px solid {colors["border"]};
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }}
            QLabel {{
                color: {colors["text"]};
            }}
            QPushButton {{
                background-color: {colors["button_bg"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 4px;
                padding: 2px 7px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {colors["button_hover"]};
            }}
            QPushButton:checked {{
                background-color: {active_btn_bg};
                color: {active_btn_fg};
                font-weight: 600;
                border-color: {active_btn_bg};
            }}
            QPushButton#FileBadge {{
                background-color: {badge_bg};
                border: 1px solid {badge_border};
                border-radius: 10px;
                padding: 1px 8px;
                font-size: 11px;
            }}
            QPushButton#MaskWarning {{
                background-color: {warn_bg};
                color: {warn_fg};
                border: 1px solid {warn_border};
                border-radius: 10px;
                padding: 1px 7px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton#MaskWarning:hover {{
                border-color: {warn_fg};
            }}
            QPushButton#CloseBtn:hover {{
                background-color: #ef4444;
                color: #ffffff;
                border-color: #ef4444;
            }}

            QMenu {{
                background-color: {colors["editor_bg"]};
                color: {colors["text"]};
                border: 1px solid {colors["border"]};
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 5px 20px 5px 10px;
                border-radius: 4px;
            }}
            QMenu#ToggleMenu::item {{
                padding-right: 36px;
            }}
            QMenu::item:selected {{
                background-color: {colors["button_hover"]};
            }}
            QMenu::icon {{
                padding-left: 2px;
            }}
            QMenu::separator {{
                height: 1px;
                background-color: {colors["border"]};
                margin: 4px 6px;
            }}
        """)

        # Re-render all Lucide vector icons
        self._update_button_icons()

    # ------------------ System Tray ------------------
    def _init_tray(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        if not hasattr(self, "tray") or self.tray is None:
            self.tray = QSystemTrayIcon(self)
            self.tray.setIcon(self._app_icon)
            self.tray.setToolTip("AbaqusPythonReader")
            self.tray.activated.connect(self._on_tray_activated)

        is_dark = self.config.get("dark_theme", False)
        mic = "#94a3b8" if is_dark else "#475569"

        tray_menu = QMenu()
        tray_menu.addAction(render_svg_to_icon(SVG_FRAME, color=mic, size=15), tr("tray_show_hide"), self._toggle_visibility)
        tray_menu.addAction(render_svg_to_icon(SVG_FOLDER, color=mic, size=15), tr("menu_open_file"), self._browse_file)
        tray_menu.addAction(render_svg_to_icon(SVG_RESET, color=mic, size=15), tr("menu_reset_window"), self._reset_window_geometry)
        tray_menu.addSeparator()
        tray_menu.addAction(render_svg_to_icon(SVG_QUIT, color=mic, size=15), tr("menu_quit"), self.close)

        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def _toggle_visibility(self):
        if self.isVisible() and not self.isMinimized():
            self.hide()
        else:
            self.showNormal()
            self.activateWindow()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger or reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._toggle_visibility()

    # ------------------ Smooth System Dragging & Resizing ------------------
    def _get_edge_at(self, pos: QPoint):
        m = self.RESIZE_MARGIN
        w, h = self.width(), self.height()
        edge = None

        on_left = pos.x() <= m
        on_right = pos.x() >= w - m
        on_top = pos.y() <= m
        on_bottom = pos.y() >= h - m

        if on_top and on_left:
            edge = Qt.Edge.TopEdge | Qt.Edge.LeftEdge
        elif on_top and on_right:
            edge = Qt.Edge.TopEdge | Qt.Edge.RightEdge
        elif on_bottom and on_left:
            edge = Qt.Edge.BottomEdge | Qt.Edge.LeftEdge
        elif on_bottom and on_right:
            edge = Qt.Edge.BottomEdge | Qt.Edge.RightEdge
        elif on_left:
            edge = Qt.Edge.LeftEdge
        elif on_right:
            edge = Qt.Edge.RightEdge
        elif on_top:
            edge = Qt.Edge.TopEdge
        elif on_bottom:
            edge = Qt.Edge.BottomEdge

        return edge

    def mousePressEvent(self, event):
        # 1. Right Button: Drag window anywhere (smooth delta movement)
        if event.button() == Qt.MouseButton.RightButton:
            self._right_drag_active = True
            self._right_click_pos = event.globalPosition().toPoint()
            self._window_start_pos = self.pos()
            self.setCursor(Qt.CursorShape.SizeAllCursor)
            event.accept()
            return

        # 2. Left Button: Edge resizing (native OS system resize)
        if event.button() == Qt.MouseButton.LeftButton and self.config.get("frameless", True):
            edge = self._get_edge_at(event.position().toPoint())
            if edge and self.windowHandle():
                self.windowHandle().startSystemResize(edge)
                event.accept()
                return

        # 3. Left Button: Header bar dragging (native OS system move)
        if event.button() == Qt.MouseButton.LeftButton:
            if self.top_bar.geometry().contains(event.position().toPoint()) and self.windowHandle():
                self.windowHandle().startSystemMove()
                event.accept()
                return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # Handle right button drag
        if self._right_drag_active:
            if event.buttons() & Qt.MouseButton.RightButton:
                delta = event.globalPosition().toPoint() - self._right_click_pos
                self.move(self._window_start_pos + delta)
                event.accept()
                return
            else:
                self._right_drag_active = False
                self.unsetCursor()

        # Update cursor for edges if frameless
        if self.config.get("frameless", True):
            edge = self._get_edge_at(event.position().toPoint())
            if edge == (Qt.Edge.TopEdge | Qt.Edge.LeftEdge) or edge == (Qt.Edge.BottomEdge | Qt.Edge.RightEdge):
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif edge == (Qt.Edge.TopEdge | Qt.Edge.RightEdge) or edge == (Qt.Edge.BottomEdge | Qt.Edge.LeftEdge):
                self.setCursor(Qt.CursorShape.SizeBDiagCursor)
            elif edge in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif edge in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            was_dragging = self._right_drag_active
            self._right_drag_active = False
            self.unsetCursor()

            # If user barely moved the mouse (< 4px), show context menu
            moved_dist = (event.globalPosition().toPoint() - self._right_click_pos).manhattanLength()
            if moved_dist < 4:
                self._show_context_menu(event.globalPosition().toPoint())
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def _show_context_menu(self, global_pos: QPoint):
        self._build_menu(context=True).exec(global_pos)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "toast") and self.toast and self.toast.isVisible():
            pw = self.width()
            ph = self.height()
            w = self.toast.width()
            self.toast.move((pw - w) // 2, ph - 42)
            self.toast.raise_()

    def closeEvent(self, event):
        self.config.set("window_x", self.x())
        self.config.set("window_y", self.y())
        self.config.set("window_width", self.width())
        self.config.set("window_height", self.height())
        self.file_monitor.stop()
        if hasattr(self, "tray"):
            self.tray.hide()
        event.accept()
