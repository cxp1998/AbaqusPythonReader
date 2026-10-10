import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict

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
        "title": "坐标模式 (COORDINATE / findAt 坐标)",
        "badge": "findAt 坐标",
        "tag": "强烈推荐 · 参数化建模必备",
        "command": "session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)",
        "description": "以空间坐标 findAt((x, y, z)) 方式录制几何对象。尺寸、网格变更后依然完美适配，参数化建模与优化通用性极强！",
        "example": "cells = c.findAt(((10.0, 5.0, 0.0), ))\nregion = p.Set(cells=cells, name='Set-1')",
        "icon_svg": SVG_CROSSHAIR,
        "color": "#10b981", # Emerald
    },
    MODE_INDEX: {
        "key": MODE_INDEX,
        "title": "索引模式 (INDEX / 对象索引号)",
        "badge": "序号 [0]",
        "tag": "网格/单元节点遍历利器",
        "command": "session.journalOptions.setValues(replayGeometry=INDEX, recoverGeometry=INDEX)",
        "description": "以 Python 原生列表下标索引方式 (如 e[0], c[0:5]) 录制。适合网格遍历、单元节点循环批处理与算法调试。",
        "example": "e1 = p.elements[0]\ne2 = p.elements[0:10]\nregion = p.Set(elements=e2, name='ElemSet')",
        "icon_svg": SVG_LIST_ORDERED,
        "color": "#3b82f6", # Blue
    },
    MODE_COMPRESSED: {
        "key": MODE_COMPRESSED,
        "title": "掩码模式 (COMPRESSEDINDEX / 默认掩码)",
        "badge": "默认掩码",
        "tag": "Abaqus 默认 · 不推荐二次开发",
        "command": "session.journalOptions.setValues(replayGeometry=COMPRESSEDINDEX, recoverGeometry=COMPRESSEDINDEX)",
        "description": "Abaqus 内部二进制压缩编码 (getSequenceFromMask)。不可读且无通用性，一旦修改模型尺寸或网格立即报错失效。",
        "example": "cells = c.getSequenceFromMask(mask=('[#1 ]', ), )",
        "icon_svg": SVG_TERMINAL,
        "color": "#94a3b8", # Slate
    },
}

HEADER_MARKER = "# --- PythonReader Auto-Generated: Abaqus Journal Options ---"
FOOTER_MARKER = "# --- End PythonReader Auto-Generated ---"


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
def get_env_paths(project_dir: Optional[str] = None) -> Dict[str, Path]:
    """Returns candidate paths for abaqus_v6.env."""
    proj = Path(project_dir) if project_dir else Path.cwd()
    return {
        "project": proj / "abaqus_v6.env",
        "user": Path.home() / "abaqus_v6.env"
    }


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
            f"    # PythonReader: Auto configured {mode} journal mode\n"
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
        return True, f"成功配置到:\n{filepath}"
    except Exception as e:
        return False, f"写入配置文件失败: {e}"


def remove_env_file_mode(filepath: Path) -> Tuple[bool, str]:
    """Removes our onCaeStartup block from abaqus_v6.env."""
    if not filepath.exists():
        return True, "文件不存在，无需清除"
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
            return True, f"已清除配置并移除文件:\n{filepath}"
        else:
            filepath.write_text(cleaned + "\n", encoding="utf-8")
            return True, f"已从配置文件中清除 PythonReader 启动项:\n{filepath}"
    except Exception as e:
        return False, f"清除失败: {e}"


# -------------------------------------------------------------
# Mode Selector & Injector Dialog
# -------------------------------------------------------------
class AbaqusModeDialog(QDialog):
    """Modern HUD dialog to switch Abaqus recording mode."""

    def __init__(self, parent=None, is_dark=False, project_dir=None):
        super().__init__(parent)
        self.is_dark = is_dark
        self.project_dir = project_dir or os.getcwd()
        self.selected_mode = MODE_COORDINATE
        self.env_paths = get_env_paths(self.project_dir)

        self.setWindowTitle("Abaqus 录制格式配置 (坐标 / 索引 / 掩码)")
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
        lbl_title = QLabel("Abaqus CAE 命令流索引模式管理")
        lbl_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_sub = QLabel("避免 getSequenceFromMask 掩码，将输出切换为空间坐标 (findAt) 或数组序号 (INDEX)")
        lbl_sub.setFont(QFont("Segoe UI", 9))
        lbl_sub.setStyleSheet("color: #64748b;")
        title_box.addWidget(lbl_title)
        title_box.addWidget(lbl_sub)
        header.addLayout(title_box)
        header.addStretch()

        btn_help = QPushButton("说明指南")
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
        lbl_sec1 = QLabel("1. 选择目标录制格式 (实时复制或写入配置)")
        lbl_sec1.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec1)

        self.btn_group = QButtonGroup(self)
        self.cards = {}

        for mode_key in [MODE_COORDINATE, MODE_INDEX, MODE_COMPRESSED]:
            card = self._create_mode_card(mode_key)
            layout.addWidget(card)
            self.cards[mode_key] = card

        # 3. Action Buttons for Current Running Abaqus
        lbl_sec2 = QLabel("2. 对当前正在运行的 Abaqus/CAE 生效")
        lbl_sec2.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec2)

        action_box = QHBoxLayout()
        action_box.setSpacing(10)

        self.btn_copy_inject = QPushButton(" 一键复制指令并聚焦 Abaqus")
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

        self.lbl_abq_status = QLabel("正在检测 Abaqus...")
        self.lbl_abq_status.setFont(QFont("Segoe UI", 9))
        action_box.addWidget(self.lbl_abq_status)
        action_box.addStretch()
        layout.addLayout(action_box)

        # 4. Section B: Persistent Startup Configuration (abaqus_v6.env)
        lbl_sec3 = QLabel("3. 永久生效配置 (写入 abaqus_v6.env，每次启动软件自动生效)")
        lbl_sec3.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        layout.addWidget(lbl_sec3)

        env_group = QGroupBox()
        env_group.setStyleSheet("QGroupBox { border: 1px solid #cbd5e1; border-radius: 6px; padding: 10px; }")
        env_vbox = QVBoxLayout(env_group)
        env_vbox.setSpacing(8)

        # Radio for Scope
        scope_hbox = QHBoxLayout()
        self.rb_scope_proj = QRadioButton("当前工程目录 (仅对当前目录生效)")
        self.rb_scope_user = QRadioButton("用户主目录 (全局所有新建和运行工程自动生效)")
        self.rb_scope_proj.setChecked(True)
        scope_hbox.addWidget(self.rb_scope_proj)
        scope_hbox.addWidget(self.rb_scope_user)
        scope_hbox.addStretch()
        env_vbox.addLayout(scope_hbox)

        # Status text
        self.lbl_env_status = QLabel("配置文件状态...")
        self.lbl_env_status.setFont(QFont("Segoe UI", 8))
        self.lbl_env_status.setStyleSheet("color: #64748b;")
        env_vbox.addWidget(self.lbl_env_status)

        # Env buttons
        env_btns = QHBoxLayout()
        self.btn_save_env = QPushButton(" 设为启动默认 (写入配置)")
        self.btn_save_env.setIcon(render_svg_to_icon(SVG_SHIELD_CHECK, color="#059669", size=14))
        self.btn_save_env.clicked.connect(self._save_env_config)
        env_btns.addWidget(self.btn_save_env)

        self.btn_remove_env = QPushButton(" 清除自动配置")
        self.btn_remove_env.setIcon(render_svg_to_icon(SVG_CLOSE, color="#ef4444", size=13))
        self.btn_remove_env.clicked.connect(self._clear_env_config)
        env_btns.addWidget(self.btn_remove_env)

        self.btn_open_folder = QPushButton(" 打开所在文件夹")
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

        self.rb_scope_proj.toggled.connect(self._refresh_status)
        self.rb_scope_user.toggled.connect(self._refresh_status)

    def _create_mode_card(self, mode_key: str) -> QWidget:
        info = MODE_INFO[mode_key]
        card = QFrame()
        card.setObjectName(f"Card_{mode_key}")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                background-color: #f8fafc;
                padding: 4px;
            }
        """)

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
            if key == self.selected_mode:
                card.setStyleSheet("""
                    QFrame {
                        border: 2px solid #2563eb;
                        border-radius: 6px;
                        background-color: #eff6ff;
                        padding: 4px;
                    }
                """)
            else:
                card.setStyleSheet("""
                    QFrame {
                        border: 1px solid #cbd5e1;
                        border-radius: 6px;
                        background-color: #f8fafc;
                        padding: 4px;
                    }
                """)

    def _refresh_status(self):
        self._highlight_selected_card()

        # Abaqus process / window detection
        is_running = check_abaqus_process_running()
        hwnd = find_abaqus_window()
        if hwnd:
            self.lbl_abq_status.setText("● 检测到 Abaqus/CAE 窗口 (已就绪)")
            self.lbl_abq_status.setStyleSheet("color: #059669; font-weight: 600;")
        elif is_running:
            self.lbl_abq_status.setText("● 检测到 Abaqus 进程在后台运行")
            self.lbl_abq_status.setStyleSheet("color: #0284c7; font-weight: 600;")
        else:
            self.lbl_abq_status.setText("○ 未检测到 Abaqus/CAE 运行")
            self.lbl_abq_status.setStyleSheet("color: #94a3b8;")

        # Env file detection
        target_path = self.env_paths["user"] if self.rb_scope_user.isChecked() else self.env_paths["project"]
        current_env_mode = detect_env_file_mode(target_path)
        if current_env_mode:
            mode_name = MODE_INFO.get(current_env_mode, {}).get("badge", current_env_mode)
            self.lbl_env_status.setText(f"当前文件: {target_path}\n已配置模式: 【{mode_name}】(每次启动 CAE 自动运行)")
            self.lbl_env_status.setStyleSheet("color: #059669; font-weight: 500;")
        elif target_path.exists():
            self.lbl_env_status.setText(f"当前文件: {target_path}\n文件存在但未配置 journalOptions 自动启动项")
            self.lbl_env_status.setStyleSheet("color: #d97706;")
        else:
            self.lbl_env_status.setText(f"目标路径: {target_path} (尚未创建，点击下方按钮一键生成)")
            self.lbl_env_status.setStyleSheet("color: #64748b;")

    def _copy_and_focus(self):
        info = MODE_INFO[self.selected_mode]
        cmd = info["command"]
        QApplication.clipboard().setText(cmd)

        hwnd = find_abaqus_window()
        focus_msg = ""
        if hwnd:
            activate_abaqus_window(hwnd)
            focus_msg = "已将 Abaqus CAE 窗口激活并置于前台！\n"

        QMessageBox.information(
            self,
            "指令已复制",
            f"已成功将【{info['badge']}】指令复制到剪贴板！\n\n"
            f"命令流:\n{cmd}\n\n"
            f"{focus_msg}"
            f"👉 使用方式：\n"
            f"在 Abaqus 界面最下方的命令行交互行 (>>>) 处直接按 Ctrl+V 粘贴并回车，"
            f"之后的所有操作就会立即以该格式输出到 rpy/rec 文件中！"
        )

    def _save_env_config(self):
        target_path = self.env_paths["user"] if self.rb_scope_user.isChecked() else self.env_paths["project"]
        ok, msg = write_env_file_mode(target_path, self.selected_mode)
        if ok:
            QMessageBox.information(
                self,
                "配置成功",
                f"{msg}\n\n"
                f"已写入 onCaeStartup 钩子函数。\n"
                f"以后启动 Abaqus/CAE 时，将自动以【{MODE_INFO[self.selected_mode]['badge']}】格式录制，再也不用手动敲命令了！"
            )
        else:
            QMessageBox.critical(self, "配置失败", msg)
        self._refresh_status()

    def _clear_env_config(self):
        target_path = self.env_paths["user"] if self.rb_scope_user.isChecked() else self.env_paths["project"]
        ok, msg = remove_env_file_mode(target_path)
        if ok:
            QMessageBox.information(self, "清除成功", msg)
        else:
            QMessageBox.critical(self, "清除失败", msg)
        self._refresh_status()

    def _open_env_dir(self):
        target_path = self.env_paths["user"] if self.rb_scope_user.isChecked() else self.env_paths["project"]
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
        self.setWindowTitle("Abaqus 二次开发：实体索引与坐标模式全攻略")
        self.resize(680, 520)
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
        btn_close = QPushButton("我知道了")
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
            h2 { color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 4px; margin-top: 10px; }
            h3 { color: #1e40af; margin-top: 14px; margin-bottom: 4px; }
            p { margin: 6px 0; }
            code { background-color: #f1f5f9; color: #0f766e; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; font-size: 12px; }
            pre { background-color: #0f172a; color: #f8fafc; padding: 10px 14px; border-radius: 6px; font-family: Consolas, monospace; font-size: 12px; overflow-x: auto; }
            .tip { background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 8px 12px; border-radius: 4px; margin: 8px 0; }
            .warn { background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 8px 12px; border-radius: 4px; margin: 8px 0; }
            table { border-collapse: collapse; width: 100%; margin: 10px 0; }
            th, td { border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; font-size: 12px; }
            th { background-color: #f8fafc; }
        </style>
        </head>
        <body>
            <h2>为什么二次开发中应坚决避免 <code>getSequenceFromMask</code>？</h2>
            <div class="warn">
                <b>掩码的致命缺陷：</b><br/>
                在 Abaqus/CAE 中选择面、边、体或单元时，默认会生成如 <code>c.getSequenceFromMask(mask=('[#1 ]', ), )</code> 的掩码指令。
                掩码是 Abaqus 内部对当前拓扑 ID 的二进制哈希压缩，<b>完全没有几何语义</b>。
                一旦修改零件的长宽高尺寸、变更圆角、或者更改网格密度，实体的内部编号全部改变，原有的掩码将直接<b>选错对象或抛出 KeyError 异常导致脚本崩溃</b>！
            </div>

            <h2>Abaqus 提供的三种实体索引方式对比</h2>
            <table>
                <tr>
                    <th>方式</th>
                    <th>对应指令 / 格式</th>
                    <th>适用场景与优缺点</th>
                </tr>
                <tr>
                    <td><b>1. 掩码模式</b><br/>(默认)</td>
                    <td><code>COMPRESSEDINDEX</code><br/><code>getSequenceFromMask(...)</code></td>
                    <td><b>缺点：</b>不可读、无参数化通用性，模型修改即失效。<br/><b>优点：</b>仅对单次静态回放占用文本体积小。</td>
                </tr>
                <tr>
                    <td><b>2. 坐标模式</b><br/>(强烈推荐)</td>
                    <td><code>COORDINATE</code><br/><code>findAt(((x, y, z), ))</code></td>
                    <td><b>优点：</b>使用实体空间 3D 坐标唯一定位。在参数化脚本中，可通过变量直接推导坐标 (例如板中心 <code>(L/2, W/2, H)</code>)，鲁棒性极高，尺寸任意修改绝不报错！</td>
                </tr>
                <tr>
                    <td><b>3. 索引号模式</b></td>
                    <td><code>INDEX</code><br/><code>p.elements[0], p.cells[0:10]</code></td>
                    <td><b>优点：</b>原生 Python 列表切片语法。适合批量遍历所有网格单元、节点集合或进行算法运算。</td>
                </tr>
            </table>

            <h2>如何让当前运行中的 Abaqus 立即生效？</h2>
            <p>打开 Abaqus/CAE 窗口，在屏幕最下方的<b>命令行交互行 (>>>)</b> 中输入以下指令并回车：</p>
            <h3>选项 A：切换为坐标模式 (findAt)</h3>
            <pre>session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)</pre>

            <h3>选项 B：切换为实际索引号模式 (INDEX)</h3>
            <pre>session.journalOptions.setValues(replayGeometry=INDEX, recoverGeometry=INDEX)</pre>

            <div class="tip">
                <b>生效效果：</b><br/>
                执行后，后续你在 Abaqus 界面所做的所有几何选择、面载荷施加、截面指派，写入 <code>abaqus.rpy</code> 和 <code>abaqus.rec</code> 时就会自动变成清晰的坐标或切片语法！
            </div>

            <h2>如何一劳永逸：配置 <code>abaqus_v6.env</code> 启动永久自动执行</h2>
            <p>你无需每次打开 Abaqus 都敲一遍命令。Abaqus 提供了 <code>onCaeStartup</code> 启动钩子：</p>
            <p>在当前工程目录或用户主目录（<code>~ / abaqus_v6.env</code>）添加：</p>
            <pre>def onCaeStartup():
    session.journalOptions.setValues(
        replayGeometry=COORDINATE,
        recoverGeometry=COORDINATE
    )</pre>
            <p>在 PythonReader 的【录制格式配置】窗口中，点击<b>【设为启动默认】</b>即可一键自动写入，零配置门槛！</p>
        </body>
        </html>
        """
