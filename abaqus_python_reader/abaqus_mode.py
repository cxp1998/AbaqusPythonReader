import re
import sys
from pathlib import Path
from typing import Optional, Tuple

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QGroupBox,
    QTextBrowser, QMessageBox, QApplication, QFrame,
    QFileDialog
)
from PySide6.QtGui import QFont, QIcon, QColor, QDesktopServices
from PySide6.QtCore import Qt, QUrl

from .icons import (
    render_svg_to_icon,
    SVG_CROSSHAIR, SVG_LIST_ORDERED, SVG_TERMINAL,
    SVG_SETTINGS, SVG_BOOK_OPEN, SVG_CHECK, SVG_COPY,
    SVG_ALERT_TRIANGLE, SVG_FOLDER, SVG_SHIELD_CHECK, SVG_CLOSE
)

# -------------------------------------------------------------
# Mode Definitions
# -------------------------------------------------------------
MODE_COORDINATE = "COORDINATE"
MODE_INDEX = "INDEX"
MODE_COMPRESSED = "COMPRESSEDINDEX"

MODE_INFO = {
    MODE_COORDINATE: {
        "key": MODE_COORDINATE,
        "title": "坐标（COORDINATE）",
        "badge": "坐标",
        "tag": "推荐",
        "command": "session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)",
        "description": "findAt((x, y, z))，模型修改后仍可用，适合参数化建模。",
        "example": "cells = c.findAt(((10.0, 5.0, 0.0), ))\nregion = p.Set(cells=cells, name='Set-1')",
        "icon_svg": SVG_CROSSHAIR,
        "color": "#10b981", # Emerald
    },
    MODE_INDEX: {
        "key": MODE_INDEX,
        "title": "索引（INDEX）",
        "badge": "索引",
        "tag": "",
        "command": "session.journalOptions.setValues(replayGeometry=INDEX, recoverGeometry=INDEX)",
        "description": "e[0]、c[0:5]，适合遍历单元和节点。",
        "example": "e1 = p.elements[0]\ne2 = p.elements[0:10]\nregion = p.Set(elements=e2, name='ElemSet')",
        "icon_svg": SVG_LIST_ORDERED,
        "color": "#3b82f6", # Blue
    },
    MODE_COMPRESSED: {
        "key": MODE_COMPRESSED,
        "title": "掩码（COMPRESSEDINDEX）",
        "badge": "掩码",
        "tag": "默认",
        "command": "session.journalOptions.setValues(replayGeometry=COMPRESSEDINDEX, recoverGeometry=COMPRESSEDINDEX)",
        "description": "getSequenceFromMask，模型修改后失效。",
        "example": "cells = c.getSequenceFromMask(mask=('[#1 ]', ), )",
        "icon_svg": SVG_TERMINAL,
        "color": "#94a3b8", # Slate
    },
}

HEADER_MARKER = "# --- AbaqusPythonReader Auto-Generated: Abaqus Journal Options ---"
FOOTER_MARKER = "# --- End AbaqusPythonReader Auto-Generated ---"


# -------------------------------------------------------------
# Abaqus Window & Process Helpers
# -------------------------------------------------------------
def check_abaqus_process_running() -> bool:
    """Checks if any Abaqus process is running."""
    if sys.platform != "win32":
        return False
    try:
        import ctypes
        from ctypes import wintypes
        kernel32 = ctypes.windll.kernel32
        
        TH32CS_SNAPPROCESS = 0x00000002
        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD),
                ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD),
                ("th32DefaultHeapID", ctypes.c_void_p),
                ("th32ModuleID", wintypes.DWORD),
                ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD),
                ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", wintypes.DWORD),
                ("szExeFile", ctypes.c_wchar * 260)
            ]
        
        h_snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if h_snap == -1:
            return False
            
        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
        
        running = False
        if kernel32.Process32FirstW(h_snap, ctypes.byref(pe)):
            while True:
                name = pe.szExeFile.lower()
                if "abqcae" in name or name in ("abaqus.exe", "abqcaeg.exe", "abqcaek.exe"):
                    running = True
                    break
                if not kernel32.Process32NextW(h_snap, ctypes.byref(pe)):
                    break
        kernel32.CloseHandle(h_snap)
        return running
    except Exception:
        return False


def find_abaqus_window() -> Optional[int]:
    """Finds top-level window handle for running Abaqus/CAE."""
    if sys.platform != "win32":
        return None
    try:
        import ctypes
        user32 = ctypes.windll.user32
        
        found_hwnd = None
        def enum_cb(hwnd, _):
            nonlocal found_hwnd
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value.lower()
                    if ("abaqus/cae" in title or "simulia abaqus" in title or 
                        ("abaqus" in title and "viewer" not in title and "pythonreader" not in title)):
                        found_hwnd = hwnd
                        return False # Stop enum
            return True

        LPARAM = ctypes.c_ssize_t
        HWND = ctypes.c_void_p
        BOOL = ctypes.c_bool
        WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
        user32.EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
        user32.EnumWindows.restype = BOOL
        user32.EnumWindows(WNDENUMPROC(enum_cb), 0)
        return found_hwnd
    except Exception:
        return None


def activate_abaqus_window(hwnd: int) -> bool:
    """Brings Abaqus window to foreground."""
    if sys.platform != "win32" or not hwnd:
        return False
    try:
        import ctypes
        user32 = ctypes.windll.user32
        user32.ShowWindow(hwnd, 9) # SW_RESTORE
        return bool(user32.SetForegroundWindow(hwnd))
    except Exception:
        return False


# -------------------------------------------------------------
# abaqus_v6.env Configuration Helpers
# -------------------------------------------------------------
def get_env_path() -> Path:
    """Returns the user-level abaqus_v6.env, which applies to every Abaqus/CAE session."""
    return Path.home() / "abaqus_v6.env"


def detect_env_file_mode(filepath: Path) -> Optional[str]:
    """Reads abaqus_v6.env and detects configured mode."""
    if not filepath.exists():
        return None
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"replayGeometry\s*=\s*COORDINATE", content):
            return MODE_COORDINATE
        if re.search(r"replayGeometry\s*=\s*INDEX", content):
            return MODE_INDEX
        if re.search(r"replayGeometry\s*=\s*COMPRESSEDINDEX", content):
            return MODE_COMPRESSED
    except Exception:
        pass
    return None


def write_env_file_mode(filepath: Path, mode: str) -> Tuple[bool, str]:
    """Safely updates or appends onCaeStartup hook to abaqus_v6.env."""
    try:
        content = ""
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8", errors="ignore")

        # Strip our previous auto-generated block if exists
        pattern = re.compile(
            re.escape(HEADER_MARKER) + r".*?" + re.escape(FOOTER_MARKER) + r"\n?",
            re.DOTALL
        )
        content = pattern.sub("", content).strip()

        block = (
            f"\n\n{HEADER_MARKER}\n"
            f"def onCaeStartup():\n"
            f"    # AbaqusPythonReader: Auto configured {mode} journal mode\n"
            f"    try:\n"
            f"        session.journalOptions.setValues(\n"
            f"            replayGeometry={mode},\n"
            f"            recoverGeometry={mode}\n"
            f"        )\n"
            f"    except Exception:\n"
            f"        pass\n"
            f"{FOOTER_MARKER}\n"
        )
        new_content = (content + block).strip() + "\n"
        filepath.write_text(new_content, encoding="utf-8")
        return True, f"已写入：\n{filepath}"
    except Exception as e:
        return False, f"写入失败：{e}"


def remove_env_file_mode(filepath: Path) -> Tuple[bool, str]:
    """Removes our onCaeStartup block from abaqus_v6.env."""
    if not filepath.exists():
        return True, "配置文件不存在"
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        pattern = re.compile(
            re.escape(HEADER_MARKER) + r".*?" + re.escape(FOOTER_MARKER) + r"\n?",
            re.DOTALL
        )
        cleaned = pattern.sub("", content).strip()
        if not cleaned:
            # File was only our block, remove it cleanly
            filepath.unlink()
            return True, f"已删除：\n{filepath}"
        else:
            filepath.write_text(cleaned + "\n", encoding="utf-8")
            return True, f"已清除：\n{filepath}"
    except Exception as e:
        return False, f"清除失败：{e}"


# -------------------------------------------------------------
# Mode Selector & Injector Dialog
# -------------------------------------------------------------
class AbaqusModeDialog(QDialog):
    """Modern HUD dialog to switch Abaqus recording mode."""

    def __init__(self, parent=None, is_dark=False):
        super().__init__(parent)
        self.is_dark = is_dark
        self.selected_mode = MODE_COORDINATE
        self.env_path = get_env_path()

        self.setWindowTitle("录制模式")
        self.setFixedWidth(560)
        self._init_ui()
        self._refresh_status()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(18, 18, 18, 18)

        # 1. Header Banner
        header = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setPixmap(render_svg_to_icon(SVG_CROSSHAIR, color="#2563eb", size=24).pixmap(24, 24))
        header.addWidget(icon_lbl)

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        lbl_title = QLabel("几何录制模式")
        lbl_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_sub = QLabel("Abaqus 在 .rpy 中记录几何对象的方式")
        lbl_sub.setFont(QFont("Segoe UI", 9))
        lbl_sub.setStyleSheet("color: #64748b;")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        header.addLayout(title_box)
        header.addStretch()

        btn_help = QPushButton("说明")
        btn_help.setIcon(render_svg_to_icon(SVG_BOOK_OPEN, color="#475569", size=14))
        btn_help.clicked.connect(self._open_guide)
        header.addWidget(btn_help)
        layout.addLayout(header)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #e2e8f0;")
        layout.addWidget(line)

        # 2. Section A: Mode Selection Cards
        lbl_sec1 = QLabel("模式")
        lbl_sec1.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec1)

        self.btn_group = QButtonGroup(self)
        self.cards = {}

        for mode_key in [MODE_COORDINATE, MODE_INDEX, MODE_COMPRESSED]:
            card = self._create_mode_card(mode_key)
            layout.addWidget(card)
            self.cards[mode_key] = card

        # 3. Action Buttons for Current Running Abaqus
        lbl_sec2 = QLabel("当前会话")
        lbl_sec2.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec2)

        action_box = QHBoxLayout()
        action_box.setSpacing(10)

        self.btn_copy_inject = QPushButton(" 复制指令并切换到 Abaqus")
        self.btn_copy_inject.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.btn_copy_inject.setIcon(render_svg_to_icon(SVG_COPY, color="#ffffff", size=15))
        self.btn_copy_inject.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                padding: 6px 14px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover { background-color: #1d4ed8; }
        """)
        self.btn_copy_inject.clicked.connect(self._copy_and_focus)
        action_box.addWidget(self.btn_copy_inject)

        self.lbl_abq_status = QLabel("")
        self.lbl_abq_status.setFont(QFont("Segoe UI", 9))
        action_box.addWidget(self.lbl_abq_status)
        action_box.addStretch()
        layout.addLayout(action_box)

        # 4. Section B: Persistent Startup Configuration (abaqus_v6.env)
        lbl_sec3 = QLabel("启动默认")
        lbl_sec3.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec3)

        env_group = QGroupBox()
        env_group.setStyleSheet("QGroupBox { border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; }")
        env_vbox = QVBoxLayout(env_group)
        env_vbox.setSpacing(8)

        # Status text
        self.lbl_env_status = QLabel("")
        self.lbl_env_status.setFont(QFont("Segoe UI", 8))
        self.lbl_env_status.setStyleSheet("color: #64748b;")
        env_vbox.addWidget(self.lbl_env_status)

        # Env buttons
        env_btns = QHBoxLayout()
        self.btn_save_env = QPushButton(" 写入")
        self.btn_save_env.setIcon(render_svg_to_icon(SVG_SHIELD_CHECK, color="#059669", size=14))
        self.btn_save_env.clicked.connect(self._save_env_config)
        env_btns.addWidget(self.btn_save_env)

        self.btn_remove_env = QPushButton(" 清除")
        self.btn_remove_env.setIcon(render_svg_to_icon(SVG_CLOSE, color="#ef4444", size=13))
        self.btn_remove_env.clicked.connect(self._clear_env_config)
        env_btns.addWidget(self.btn_remove_env)

        self.btn_open_folder = QPushButton(" 打开目录")
        self.btn_open_folder.setIcon(render_svg_to_icon(SVG_FOLDER, color="#475569", size=14))
        self.btn_open_folder.clicked.connect(self._open_env_dir)
        env_btns.addWidget(self.btn_open_folder)

        env_btns.addStretch()
        env_vbox.addLayout(env_btns)
        layout.addWidget(env_group)

        # 5. Bottom Close Button
        bottom_box = QHBoxLayout()
        bottom_box.addStretch()
        btn_close = QPushButton("关闭")
        btn_close.setFixedWidth(80)
        btn_close.clicked.connect(self.accept)
        bottom_box.addWidget(btn_close)
        layout.addLayout(bottom_box)

    def _create_mode_card(self, mode_key: str) -> QWidget:
        info = MODE_INFO[mode_key]
        card = QFrame()
        card.setObjectName(f"Card_{mode_key}")
        card.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(10)

        rb = QRadioButton()
        rb.setChecked(mode_key == MODE_COORDINATE)
        self.btn_group.addButton(rb)
        rb.toggled.connect(lambda checked, m=mode_key: self._on_mode_toggled(m, checked))
        layout.addWidget(rb)

        content = QVBoxLayout()
        content.setSpacing(2)

        header = QHBoxLayout()
        lbl_title = QLabel(info["title"])
        lbl_title.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        header.addWidget(lbl_title)

        if info["tag"]:
            lbl_badge = QLabel(f" {info['tag']} ")
            lbl_badge.setFont(QFont("Segoe UI", 8))
            lbl_badge.setStyleSheet(f"background-color: {info['color']}; color: #ffffff; border-radius: 3px; padding: 1px 4px;")
            header.addWidget(lbl_badge)
        header.addStretch()
        content.addLayout(header)

        lbl_desc = QLabel(info["description"])
        lbl_desc.setWordWrap(True)
        lbl_desc.setFont(QFont("Segoe UI", 8))
        lbl_desc.setStyleSheet("color: #475569;")
        content.addWidget(lbl_desc)

        layout.addLayout(content)
        return card

    def _on_mode_toggled(self, mode_key: str, checked: bool):
        if checked:
            self.selected_mode = mode_key
            self._highlight_selected_card()

    def _highlight_selected_card(self):
        for key, card in self.cards.items():
            selected = key == self.selected_mode
            # Scope by object name: QLabel inherits QFrame and would otherwise get the border too
            card.setStyleSheet(f"""
                QFrame#{card.objectName()} {{
                    border: {"2px solid #2563eb" if selected else "1px solid #cbd5e1"};
                    border-radius: 6px;
                    background-color: {"#eff6ff" if selected else "#f8fafc"};
                    padding: 4px;
                }}
            """)

    def _refresh_status(self):
        self._highlight_selected_card()

        # Abaqus process / window detection
        is_running = check_abaqus_process_running()
        hwnd = find_abaqus_window()
        if hwnd:
            self.lbl_abq_status.setText("● Abaqus/CAE 已运行")
            self.lbl_abq_status.setStyleSheet("color: #059669; font-weight: 600;")
        elif is_running:
            self.lbl_abq_status.setText("● Abaqus 进程运行中（未找到窗口）")
            self.lbl_abq_status.setStyleSheet("color: #0284c7; font-weight: 600;")
        else:
            self.lbl_abq_status.setText("○ 未检测到 Abaqus/CAE")
            self.lbl_abq_status.setStyleSheet("color: #94a3b8;")

        # Env file detection
        target_path = self.env_path
        current_env_mode = detect_env_file_mode(target_path)
        if current_env_mode:
            mode_name = MODE_INFO.get(current_env_mode, {}).get("badge", current_env_mode)
            self.lbl_env_status.setText(f"{target_path}\n已设置：{mode_name}")
            self.lbl_env_status.setStyleSheet("color: #059669; font-weight: 500;")
        elif target_path.exists():
            self.lbl_env_status.setText(f"{target_path}\n未设置")
            self.lbl_env_status.setStyleSheet("color: #d97706;")
        else:
            self.lbl_env_status.setText(f"{target_path}\n未设置")
            self.lbl_env_status.setStyleSheet("color: #64748b;")

    def _copy_and_focus(self):
        info = MODE_INFO[self.selected_mode]
        QApplication.clipboard().setText(info["command"])

        hwnd = find_abaqus_window()
        if hwnd:
            activate_abaqus_window(hwnd)
            return

        QMessageBox.information(
            self,
            "已复制",
            f"{info['command']}\n\n在 Abaqus/CAE 命令行（>>>）中粘贴并回车即可生效。"
        )

    def _save_env_config(self):
        target_path = self.env_path
        ok, msg = write_env_file_mode(target_path, self.selected_mode)
        if ok:
            QMessageBox.information(
                self,
                "已写入",
                f"{msg}\n\n之后启动 Abaqus/CAE 时自动使用{MODE_INFO[self.selected_mode]['badge']}模式。"
            )
        else:
            QMessageBox.critical(self, "写入失败", msg)
        self._refresh_status()

    def _clear_env_config(self):
        target_path = self.env_path
        ok, msg = remove_env_file_mode(target_path)
        if ok:
            QMessageBox.information(self, "已清除", msg)
        else:
            QMessageBox.critical(self, "清除失败", msg)
        self._refresh_status()

    def _open_env_dir(self):
        target_path = self.env_path
        folder = target_path.parent
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _open_guide(self):
        dlg = AbaqusGuideDialog(self, is_dark=self.is_dark)
        dlg.exec()


# -------------------------------------------------------------
# Rich Educational Guide Dialog
# -------------------------------------------------------------
class AbaqusGuideDialog(QDialog):
    """Rich interactive markdown/HTML guide explaining Abaqus indexing strategies."""

    def __init__(self, parent=None, is_dark=False):
        super().__init__(parent)
        self.setWindowTitle("录制模式说明")
        self.resize(560, 400)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setHtml(self._get_guide_html())
        layout.addWidget(browser)

        btn_box = QHBoxLayout()
        btn_box.addStretch()
        btn_close = QPushButton("关闭")
        btn_close.setFixedWidth(90)
        btn_close.clicked.connect(self.accept)
        btn_box.addWidget(btn_close)
        layout.addLayout(btn_box)

    def _get_guide_html(self) -> str:
        return """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 13px; line-height: 1.6; color: #1e293b; }
            p { margin: 6px 0; }
            code { background-color: #f1f5f9; color: #0f766e; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; font-size: 12px; }
            pre { background-color: #0f172a; color: #f8fafc; padding: 10px 14px; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px; overflow-x: auto; }
            table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            th, td { border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; font-size: 12px; }
            th { background-color: #f8fafc; }
        </style>
        </head>
        <body>
            <p>Abaqus/CAE 默认以掩码（<code>getSequenceFromMask</code>）记录选中的几何对象。
            掩码依赖内部编号，修改尺寸或网格后会选错对象或报错。编写脚本时建议使用坐标模式。</p>
            <table>
                <tr><th>模式</th><th>示例</th><th>适用</th></tr>
                <tr><td>坐标</td><td><code>findAt(((x, y, z), ))</code></td><td>参数化建模</td></tr>
                <tr><td>索引</td><td><code>p.elements[0:10]</code></td><td>遍历单元、节点</td></tr>
                <tr><td>掩码</td><td><code>getSequenceFromMask(...)</code></td><td>Abaqus 默认</td></tr>
            </table>
            <p>在 Abaqus/CAE 命令行中手动切换：</p>
            <pre>session.journalOptions.setValues(
    replayGeometry=COORDINATE, recoverGeometry=COORDINATE)</pre>
        </body>
        </html>
        """
