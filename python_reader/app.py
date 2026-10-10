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
    Qt, QPoint, QSize, QTimer, QByteArray
)
from PySide6.QtSvg import QSvgRenderer

from .config import ConfigManager
from .file_monitor import FileMonitor
from .cleaner import clean_abaqus_script, has_mask_statement
from .editor import CodeEditor
from .highlighter import THEMES
from .icons import (
    render_svg_to_icon, render_svg_to_pixmap, get_app_logo_pixmap,
    SVG_APP_LOGO,
    SVG_SUN, SVG_MOON, SVG_COPY, SVG_CHECK, SVG_PIN, SVG_FILTER,
    SVG_MORE, SVG_CLOSE, SVG_CLEAR, SVG_SAVE, SVG_FOLDER,
    SVG_WRAP, SVG_SCROLL, SVG_HASH, SVG_FRAME, SVG_OPACITY,
    SVG_RESET, SVG_INFO, SVG_QUIT,
    SVG_CROSSHAIR, SVG_LIST_ORDERED, SVG_ALERT_TRIANGLE,
    SVG_SETTINGS, SVG_BOOK_OPEN, SVG_TERMINAL
)
from .abaqus_mode import (
    MODE_COORDINATE, MODE_INDEX, MODE_COMPRESSED, MODE_INFO,
    AbaqusModeDialog, AbaqusGuideDialog,
    find_abaqus_window, activate_abaqus_window
)


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


class MainWindow(QMainWindow):
    RESIZE_MARGIN = 6

    def __init__(self):
        super().__init__()
        self.config = ConfigManager()
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
        self.setWindowTitle("PythonReader")

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

        # Unified Logo Icon (Matches External App Icon perfectly)
        self.lbl_logo = QLabel()
        self.lbl_logo.setFixedSize(18, 18)
        self.lbl_logo.setScaledContents(True)
        layout.addWidget(self.lbl_logo)

        # App Title
        self.lbl_title = QLabel("PythonReader")
        self.lbl_title.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        layout.addWidget(self.lbl_title)

        # File Badge Button (Clean Pill: status dot + file name)
        self.btn_file = QPushButton("● abaqus.rpy")
        self.btn_file.setObjectName("FileBadge")
        self.btn_file.setToolTip("点击切换要监控的 Abaqus 脚本文件 (.rpy / .jnl / .py)")
        self.btn_file.clicked.connect(self._browse_file)
        layout.addWidget(self.btn_file)

        # Mask Warning Badge (Shown when getSequenceFromMask is detected)
        self.btn_mask_warning = QPushButton("掩码⚠️")
        self.btn_mask_warning.setObjectName("MaskWarning")
        self.btn_mask_warning.setToolTip("检测到 getSequenceFromMask 掩码！点击一键切换为坐标 (findAt) 或索引模式")
        self.btn_mask_warning.clicked.connect(self._show_abaqus_mode_dialog)
        self.btn_mask_warning.hide()
        layout.addWidget(self.btn_mask_warning)

        layout.addStretch()

        # 0. 录制格式切换 (坐标/索引/掩码)
        self.btn_mode = QPushButton("录制格式")
        self.btn_mode.setToolTip("切换 Abaqus 输出格式 (避免 getSequenceFromMask 掩码，切换为坐标 findAt 或索引 INDEX)")
        self.btn_mode.clicked.connect(self._show_mode_menu)
        layout.addWidget(self.btn_mode)

        # 1. 过滤视口
        self.btn_filter = QPushButton("过滤")

        self.btn_filter.setCheckable(True)
        self.btn_filter.setChecked(self.config.get("filter_viewport", True))
        self.btn_filter.setToolTip("开启时自动过滤无用的视图旋转、平移、缩放命令流")
        self.btn_filter.clicked.connect(self._toggle_filter)
        self.btn_filter.toggled.connect(self._update_button_icons)
        layout.addWidget(self.btn_filter)

        # 2. 复制清洗代码
        self.btn_copy = QPushButton("复制")
        self.btn_copy.setToolTip("一键复制清洗后的有效建模命令到剪贴板")
        self.btn_copy.clicked.connect(self._copy_clean_code)
        layout.addWidget(self.btn_copy)

        # 3. 置顶
        self.btn_pin = QPushButton()
        self.btn_pin.setCheckable(True)
        self.btn_pin.setFixedWidth(28)
        self.btn_pin.setChecked(self.config.get("topmost", True))
        self.btn_pin.setToolTip("切换窗口始终置顶")
        self.btn_pin.clicked.connect(self._toggle_topmost)
        self.btn_pin.toggled.connect(self._update_button_icons)
        layout.addWidget(self.btn_pin)

        # 4. 主题切换 (Lucide Vector Sun / Moon)
        self.btn_theme = QPushButton()
        self.btn_theme.setFixedWidth(28)
        self.btn_theme.setToolTip("切换深色 / 浅色模式")
        self.btn_theme.clicked.connect(self._toggle_theme)
        layout.addWidget(self.btn_theme)

        # 5. 更多菜单 (Lucide Horizontal More)
        self.btn_more = QPushButton()
        self.btn_more.setFixedWidth(28)
        self.btn_more.setToolTip("更多功能与设置")
        self.btn_more.clicked.connect(self._show_more_menu)
        layout.addWidget(self.btn_more)

        # 6. 关闭按钮 (Lucide Close X)
        self.btn_close = QPushButton()
        self.btn_close.setFixedWidth(26)
        self.btn_close.setObjectName("CloseBtn")
        self.btn_close.setToolTip("退出")
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)

        return bar

    def _update_button_icons(self):
        """Updates all Lucide vector icons based on current theme and checked state."""
        is_dark = self.config.get("dark_theme", False)
        icon_color = "#cbd5e1" if is_dark else "#475569"

        # Unified App Logo (Matches external icon)
        self.lbl_logo.setPixmap(get_app_logo_pixmap(size=18, is_dark=is_dark))

        # Mode and Mask Warning Buttons
        self.btn_mode.setIcon(render_svg_to_icon(SVG_CROSSHAIR, color=icon_color, size=13))
        self.btn_mask_warning.setIcon(render_svg_to_icon(SVG_ALERT_TRIANGLE, color="#f59e0b" if is_dark else "#d97706", size=13))

        # Filter Button: white icon if checked (active blue bg), else normal icon_color
        filter_color = "#ffffff" if self.btn_filter.isChecked() else icon_color
        self.btn_filter.setIcon(render_svg_to_icon(SVG_FILTER, color=filter_color, size=13))


        # Copy Button: normal icon_color
        self.btn_copy.setIcon(render_svg_to_icon(SVG_COPY, color=icon_color, size=13))

        # Pin Button: white icon if checked (active blue bg), else normal icon_color
        pin_color = "#ffffff" if self.btn_pin.isChecked() else icon_color
        self.btn_pin.setIcon(render_svg_to_icon(SVG_PIN, color=pin_color, size=14))

        # Theme Icon: If currently dark, show Sun (amber); if light, show Moon (indigo)!
        theme_svg = SVG_SUN if is_dark else SVG_MOON
        theme_color = "#f59e0b" if is_dark else "#6366f1"
        self.btn_theme.setIcon(render_svg_to_icon(theme_svg, color=theme_color, size=15))

        # More and Close
        self.btn_more.setIcon(render_svg_to_icon(SVG_MORE, color=icon_color, size=14))
        self.btn_close.setIcon(render_svg_to_icon(SVG_CLOSE, color=icon_color, size=12))

    def _update_window_flags(self):
        flags = Qt.WindowType.Window
        if self.config.get("frameless", True):
            flags |= Qt.WindowType.FramelessWindowHint
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
        filename = os.path.basename(self.file_monitor.filepath) if self.file_monitor.filepath else "未选择文件"
        if is_active:
            self.btn_file.setText(f"● {filename}")
            self.btn_file.setStyleSheet("color: #059669; font-weight: 600;")
        else:
            self.btn_file.setText(f"○ {filename}")
            self.btn_file.setStyleSheet("color: #d97706; font-weight: 600;")

        self.btn_file.setToolTip(f"{msg}\n路径: {self.file_monitor.filepath}\n点击更换监控文件")

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
        self.show_toast(f"视口过滤：{'已开启 (过滤平移/缩放)' if new_val else '已关闭 (显示完整命令)'}", is_active=new_val)

    def _copy_clean_code(self):
        text = clean_abaqus_script(self.raw_text_buffer, filter_viewport=True)
        if not text.strip():
            text = self.editor.toPlainText()
        QApplication.clipboard().setText(text)

        # Temporary button feedback with Lucide check icon
        self.btn_copy.setText("已复制")
        self.btn_copy.setIcon(render_svg_to_icon(SVG_CHECK, color="#10b981", size=13))
        QTimer.singleShot(1200, self._restore_copy_button)
        self.show_toast("建模命令已复制到剪贴板", is_active=True)

    def _restore_copy_button(self):
        is_dark = self.config.get("dark_theme", False)
        icon_color = "#cbd5e1" if is_dark else "#475569"
        self.btn_copy.setText("复制")
        self.btn_copy.setIcon(render_svg_to_icon(SVG_COPY, color=icon_color, size=13))

    def _clear_view(self):
        self.raw_text_buffer = ""
        self.btn_mask_warning.hide()
        self.editor.clear()
        self.show_toast("当前视图已清空", is_active=False)

    def _toggle_topmost(self):
        new_val = self.btn_pin.isChecked()
        self.config.set("topmost", new_val)
        self._update_window_flags()
        self.show()
        self._update_button_icons()
        self.show_toast(f"窗口置顶：{'已开启' if new_val else '已关闭'}", is_active=new_val)

    def _toggle_theme(self):
        is_dark = not self.config.get("dark_theme", False)
        self.config.set("dark_theme", is_dark)
        theme_name = "dark" if is_dark else "light"
        self.editor.apply_theme(theme_name)
        self._apply_theme_style()
        self.show_toast(f"主题切换：已设为{'深色模式' if is_dark else '浅色模式'}", is_active=True)

    def _browse_file(self):
        initial_dir = os.path.dirname(self.file_monitor.filepath) if self.file_monitor.filepath else os.getcwd()
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "选择监控的 Abaqus 脚本文件",
            initial_dir,
            "ABAQUS 脚本/记录 (*.rpy *.jnl *.py);;所有文件 (*.*)"
        )
        if filepath:
            self.config.set("last_file", filepath)
            self.file_monitor.set_file(filepath)

    def _save_as_file(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "另存为 Python 脚本",
            os.getcwd(),
            "Python 脚本 (*.py);;文本文件 (*.txt);;所有文件 (*.*)"
        )
        if filepath:
            text = clean_abaqus_script(self.raw_text_buffer, filter_viewport=True)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                QMessageBox.information(self, "保存成功", f"文件已保存至:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"无法写入文件:\n{e}")

    def _show_more_menu(self):
        """Displays menu with pure Lucide icons using color-only distinction for toggle states."""
        is_dark = self.config.get("dark_theme", False)
        action_color = "#94a3b8" if is_dark else "#475569"
        color_on = "#38bdf8" if is_dark else "#0284c7"
        color_off = "#475569" if is_dark else "#cbd5e1"

        menu = QMenu(self)

        menu.addAction(render_svg_to_icon(SVG_CLEAR, color=action_color, size=15), "清空当前视图", self._clear_view)
        menu.addAction(render_svg_to_icon(SVG_SAVE, color=action_color, size=15), "另存为 Python 脚本...", self._save_as_file)
        menu.addAction(render_svg_to_icon(SVG_FOLDER, color=action_color, size=15), "更换监控文件...", self._browse_file)
        menu.addSeparator()

        # Word wrap
        is_wrap = self.config.get("word_wrap", True)
        menu.addAction(
            render_svg_to_icon(SVG_WRAP, color=color_on if is_wrap else color_off, size=15),
            "自动换行",
            lambda: self._toggle_word_wrap()
        )

        # Auto scroll
        is_scroll = self.config.get("auto_scroll", True)
        menu.addAction(
            render_svg_to_icon(SVG_SCROLL, color=color_on if is_scroll else color_off, size=15),
            "自动滚屏到底部",
            lambda: self._toggle_auto_scroll()
        )

        # Show line numbers
        is_lines = self.config.get("show_line_numbers", True)
        menu.addAction(
            render_svg_to_icon(SVG_HASH, color=color_on if is_lines else color_off, size=15),
            "显示行号",
            lambda: self._toggle_line_numbers()
        )

        # Frameless HUD
        is_frame = self.config.get("frameless", True)
        menu.addAction(
            render_svg_to_icon(SVG_FRAME, color=color_on if is_frame else color_off, size=15),
            "无边框极简 HUD 模式",
            lambda: self._toggle_frameless()
        )

        menu.addSeparator()

        # Opacity
        current_op = self.config.get("opacity", 95)
        opacity_menu = menu.addMenu(render_svg_to_icon(SVG_OPACITY, color=action_color, size=15), "窗口透明度")
        for val in [100, 95, 90, 80, 70, 60, 50]:
            act = opacity_menu.addAction(f"{val}%")
            act.setCheckable(True)
            act.setChecked(val == current_op)
            act.triggered.connect(lambda checked, v=val: self._set_opacity(v))

        menu.addSeparator()
        menu.addAction(render_svg_to_icon(SVG_CROSSHAIR, color=action_color, size=15), "Abaqus 录制格式配置 (坐标/索引)...", self._show_abaqus_mode_dialog)
        menu.addAction(render_svg_to_icon(SVG_BOOK_OPEN, color=action_color, size=15), "Abaqus 实体索引开发指南...", self._show_guide_dialog)
        menu.addSeparator()
        menu.addAction(render_svg_to_icon(SVG_RESET, color=action_color, size=15), "重置窗口位置 (居中)", self._reset_window_geometry)
        menu.addAction(render_svg_to_icon(SVG_INFO, color=action_color, size=15), "关于 PythonReader 2.0...", self._show_about)

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
        self.show_toast(f"自动换行：{'已开启' if checked else '已关闭'}", is_active=checked)

    def _toggle_auto_scroll(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("auto_scroll", True)
        self.config.set("auto_scroll", checked)
        self.editor.auto_scroll = checked
        if checked:
            self.editor.scroll_to_bottom()
        self.show_toast(f"自动滚屏：{'已开启' if checked else '已关闭'}", is_active=checked)

    def _toggle_line_numbers(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("show_line_numbers", True)
        self.config.set("show_line_numbers", checked)
        self.editor.set_line_numbers_visible(checked)
        self.show_toast(f"行号显示：{'已开启' if checked else '已关闭'}", is_active=checked)

    def _toggle_frameless(self, checked=None):
        if checked is None or isinstance(checked, QPoint) or not isinstance(checked, bool):
            checked = not self.config.get("frameless", True)
        self.config.set("frameless", checked)
        self._update_window_flags()
        self.show()
        self.show_toast(f"HUD 模式：{'已开启极简无边框' if checked else '已恢复标准窗口'}", is_active=checked)

    def _set_opacity(self, percent: int):
        self.config.set("opacity", percent)
        self.setWindowOpacity(percent / 100.0)
        self.show_toast(f"窗口透明度：已设为 {percent}%", is_active=True)

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
        self.show_toast("窗口位置已居中重置", is_active=True)

    def _show_about(self):
        QMessageBox.about(
            self,
            "关于 PythonReader 2.0",
            "<h3>PythonReader 2.0</h3>"
            "<p><b>ABAQUS CAE Python 命令流实时监视与辅助工具</b></p>"
            "<hr/>"
            "<p>• <b>原生 Python 语法高亮</b>：关键字、API、函数、字符串清晰着色。<br/>"
            "• <b>智能视口命令过滤</b>：一键剔除平移、旋转、缩放等无用冗余操作。<br/>"
            "• <b>零锁死安全读取</b>：非阻塞共享读取，绝不与 Abaqus 写文件冲突。<br/>"
            "• <b>现代轻量 HUD</b>：支持右键任意拖动、边缘拉伸、置顶、透明度调节。<br/>"
            "• <b>统一 Lucide 矢量图标</b>：全界面采用高精度统一线形图标，视网膜级锐利无模糊。</p>"
            "<hr/>"
            "<p><b>致谢 (Acknowledgments)</b><br/>"
            "特别致谢原作者：<b>焦博士</b>（邮箱：<a href='mailto:ck436@126.com'>ck436@126.com</a>）<br/>"
            "致敬其 2010 年经典原创工具及为 ABAQUS 二次开发社区作出的宝贵贡献！</p>"
        )

    def _show_mode_menu(self):
        """Displays quick menu to copy coordinate / index journal commands or configure env."""
        is_dark = self.config.get("dark_theme", False)
        mic = "#94a3b8" if is_dark else "#475569"

        menu = QMenu(self)

        menu.addAction(
            render_svg_to_icon(SVG_CROSSHAIR, color="#10b981", size=15),
            "切换为坐标模式 (findAt 坐标点) [推荐参数化]",
            lambda: self._quick_set_mode(MODE_COORDINATE)
        )
        menu.addAction(
            render_svg_to_icon(SVG_LIST_ORDERED, color="#3b82f6", size=15),
            "切换为实际索引模式 (INDEX 下标序号)",
            lambda: self._quick_set_mode(MODE_INDEX)
        )
        menu.addAction(
            render_svg_to_icon(SVG_TERMINAL, color=mic, size=15),
            "恢复掩码模式 (默认 getSequenceFromMask)",
            lambda: self._quick_set_mode(MODE_COMPRESSED)
        )
        menu.addSeparator()
        menu.addAction(
            render_svg_to_icon(SVG_SETTINGS, color=mic, size=15),
            "高级配置与永久生效 (写入 abaqus_v6.env)...",
            self._show_abaqus_mode_dialog
        )
        menu.addAction(
            render_svg_to_icon(SVG_BOOK_OPEN, color=mic, size=15),
            "Abaqus 实体索引与二次开发详解指南...",
            self._show_guide_dialog
        )

        menu.exec(self.btn_mode.mapToGlobal(QPoint(0, self.btn_mode.height() + 2)))

    def _quick_set_mode(self, mode_key: str):
        info = MODE_INFO[mode_key]
        cmd = info["command"]
        QApplication.clipboard().setText(cmd)

        hwnd = find_abaqus_window()
        focus_note = ""
        if hwnd:
            activate_abaqus_window(hwnd)
            focus_note = "\n\n已尝试将 Abaqus CAE 窗口激活并置于前台！"

        old_text = self.btn_mode.text()
        self.btn_mode.setText(f"已复制: {info['badge']}")
        self.btn_mode.setIcon(render_svg_to_icon(SVG_CHECK, color="#10b981", size=13))
        QTimer.singleShot(1800, lambda: (
            self.btn_mode.setText("录制格式"),
            self._update_button_icons()
        ))

        QMessageBox.information(
            self,
            f"已切换为【{info['badge']}】",
            f"已成功将【{info['badge']}】切换指令复制到剪贴板！{focus_note}\n\n"
            f"命令流:\n{cmd}\n\n"
            f"👉 请在 Abaqus CAE 最下方的命令行交互行 (>>>) 按 Ctrl+V 回车即刻生效！\n\n"
            f"(若想以后每次启动软件都自动生效，请点击【高级配置】写入 abaqus_v6.env)"
        )

    def _show_abaqus_mode_dialog(self):
        project_dir = os.path.dirname(self.file_monitor.filepath) if self.file_monitor.filepath else os.getcwd()
        dlg = AbaqusModeDialog(self, is_dark=self.config.get("dark_theme", False), project_dir=project_dir)
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

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self._app_icon)
        self.tray.setToolTip("PythonReader 2.0 - 实时命令流监视")

        is_dark = self.config.get("dark_theme", False)
        mic = "#94a3b8" if is_dark else "#475569"

        tray_menu = QMenu()
        act_show = tray_menu.addAction(render_svg_to_icon(SVG_FRAME, color=mic, size=15), "显示 / 隐藏窗口", self._toggle_visibility)
        act_browse = tray_menu.addAction(render_svg_to_icon(SVG_FOLDER, color=mic, size=15), "更换监控文件...", self._browse_file)
        act_reset = tray_menu.addAction(render_svg_to_icon(SVG_RESET, color=mic, size=15), "重置窗口位置 (居中)", self._reset_window_geometry)
        tray_menu.addSeparator()
        act_quit = tray_menu.addAction(render_svg_to_icon(SVG_QUIT, color=mic, size=15), "退出程序", self.close)

        self.tray.setContextMenu(tray_menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
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

            # If user barely moved the mouse (< 4px), show context menu!
            moved_dist = (event.globalPosition().toPoint() - self._right_click_pos).manhattanLength()
            if moved_dist < 4:
                self._show_context_menu(event.globalPosition().toPoint())
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def _show_context_menu(self, global_pos: QPoint):
        """Right-click context menu with pure Lucide icons and clear status indicators."""
        is_dark = self.config.get("dark_theme", False)
        action_color = "#94a3b8" if is_dark else "#475569"
        color_on = "#38bdf8" if is_dark else "#0284c7"
        color_off = "#475569" if is_dark else "#cbd5e1"

        menu = QMenu(self)
        menu.addAction(render_svg_to_icon(SVG_COPY, color=action_color, size=15), "复制清洗后的建模命令", self._copy_clean_code)
        menu.addAction(render_svg_to_icon(SVG_CLEAR, color=action_color, size=15), "清空当前视图", self._clear_view)
        menu.addSeparator()

        # Viewport filter
        is_filter = self.btn_filter.isChecked()
        menu.addAction(
            render_svg_to_icon(SVG_FILTER, color=color_on if is_filter else color_off, size=15),
            "过滤视口变换命令 (Pan/Rotate/Zoom)",
            lambda: (self.btn_filter.toggle(), self._toggle_filter())
        )

        # Word wrap
        is_wrap = self.config.get("word_wrap", True)
        menu.addAction(
            render_svg_to_icon(SVG_WRAP, color=color_on if is_wrap else color_off, size=15),
            "自动换行",
            lambda: self._toggle_word_wrap()
        )

        # Auto scroll
        is_scroll = self.config.get("auto_scroll", True)
        menu.addAction(
            render_svg_to_icon(SVG_SCROLL, color=color_on if is_scroll else color_off, size=15),
            "自动滚屏到底部",
            lambda: self._toggle_auto_scroll()
        )

        # Show line numbers
        is_lines = self.config.get("show_line_numbers", True)
        menu.addAction(
            render_svg_to_icon(SVG_HASH, color=color_on if is_lines else color_off, size=15),
            "显示行号",
            lambda: self._toggle_line_numbers()
        )

        menu.addSeparator()
        menu.addAction(render_svg_to_icon(SVG_FOLDER, color=action_color, size=15), "更换监控文件...", self._browse_file)
        menu.addAction(render_svg_to_icon(SVG_SAVE, color=action_color, size=15), "另存为 Python 脚本...", self._save_as_file)
        menu.addSeparator()

        menu.addAction(render_svg_to_icon(SVG_CROSSHAIR, color=action_color, size=15), "Abaqus 录制格式配置 (坐标/索引)...", self._show_abaqus_mode_dialog)
        menu.addAction(render_svg_to_icon(SVG_BOOK_OPEN, color=action_color, size=15), "Abaqus 实体索引开发指南...", self._show_guide_dialog)
        menu.addSeparator()

        menu.addAction(render_svg_to_icon(SVG_RESET, color=action_color, size=15), "重置窗口位置 (居中)", self._reset_window_geometry)
        menu.addAction(render_svg_to_icon(SVG_INFO, color=action_color, size=15), "关于 PythonReader 2.0...", self._show_about)
        menu.addSeparator()
        menu.addAction(render_svg_to_icon(SVG_QUIT, color=action_color, size=15), "退出程序", self.close)

        menu.exec(global_pos)

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
