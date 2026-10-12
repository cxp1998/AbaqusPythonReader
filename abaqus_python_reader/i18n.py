"""Internationalization (i18n) module for AbaqusPythonReader.

Provides multi-language support (English by default, with runtime Chinese switching).
Centralizes all user-facing strings across HUD, menus, dialogs, and notifications.
"""

from typing import Optional, Dict, Any

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
}

_current_language = DEFAULT_LANGUAGE


def get_language() -> str:
    """Returns the currently active language code ('en' or 'zh')."""
    return _current_language


def set_language(lang: str) -> None:
    """Sets the active language code."""
    global _current_language
    if lang in SUPPORTED_LANGUAGES:
        _current_language = lang
    else:
        _current_language = DEFAULT_LANGUAGE


TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        # App / Window
        "app_title": "AbaqusPythonReader",
        "no_file_selected": "No file selected",
        "btn_file_tooltip": "Change monitored file",

        # Badges & Buttons
        "btn_mask_warning": "Mask",
        "btn_mask_warning_tooltip": "Detected getSequenceFromMask; recommend switching to Coordinate or Index mode",
        "btn_filter": "Filter",
        "btn_filter_tooltip": "Hide viewport operations (pan, rotate, zoom)",
        "btn_copy": "Copy",
        "btn_copy_tooltip": "Copy code (excluding viewport operations)",
        "btn_copy_done": "Copied",
        "btn_pin_tooltip": "Always on top",
        "btn_theme_tooltip": "Toggle theme",
        "btn_more_tooltip": "More",
        "btn_minimize_tooltip": "Minimize",
        "btn_close_tooltip": "Exit",

        # Menu Actions
        "menu_copy": "Copy",
        "menu_clear": "Clear",
        "menu_open_file": "Open File...",
        "menu_save_as": "Save As...",
        "menu_hide_viewport": "Hide Viewport Operations",
        "menu_word_wrap": "Word Wrap",
        "menu_auto_scroll": "Auto Scroll",
        "menu_line_numbers": "Line Numbers",
        "menu_hover_doc": "API Tooltips",
        "menu_frameless": "Frameless",
        "menu_opacity": "Opacity",
        "menu_recording_mode": "Recording Mode",
        "menu_language": "Language",
        "menu_reset_window": "Reset Window Position",
        "menu_about": "About",
        "menu_quit": "Exit",

        # Mode Menu & Actions
        "mode_set_default": "Set as Startup Default...",
        "mode_guide": "Recording Mode Guide",
        "mode_copied_toast": "Copied {badge} command; paste and press Enter in Abaqus CLI",
        "mode_tooltip_cmd": "Copy command: {cmd}",

        # Toasts
        "toast_filter_hidden": "Viewport operations hidden",
        "toast_filter_shown": "All commands shown",
        "toast_cleared": "Cleared",
        "toast_pinned": "Pinned on top",
        "toast_unpinned": "Unpinned",
        "toast_word_wrap": "Word wrap: {state}",
        "toast_auto_scroll": "Auto scroll: {state}",
        "toast_line_numbers": "Line numbers: {state}",
        "toast_hover_doc": "API tooltips: {state}",
        "toast_frameless": "Frameless: {state}",
        "toast_opacity": "Opacity {percent}%",
        "toast_window_centered": "Window centered",
        "toast_saved": "Saved {filename}",
        "toast_lang_changed": "Language switched to English",
        "state_on": "On",
        "state_off": "Off",

        # File Dialogs & Errors
        "dlg_open_title": "Open Monitored File",
        "dlg_open_filter": "Abaqus Scripts (*.rpy *.jnl *.py);;All Files (*.*)",
        "dlg_save_title": "Save As",
        "dlg_save_filter": "Python Scripts (*.py);;Text Files (*.txt);;All Files (*.*)",
        "dlg_save_failed_title": "Save Failed",

        # About Dialog
        "about_title": "About",
        "about_desc": "Abaqus/CAE command stream real-time viewer",
        "about_author": "Rewritten from ABAQUS-PythonReader (2010) by Dr. Jiao (<a href='mailto:ck436@126.com'>ck436@126.com</a>).<br>API documentation derived from <a href='https://github.com/haiiliin/abqpy'>abqpy</a> (Hailin Wang).",
        "about_license": "MIT License",

        # Tray Menu
        "tray_show_hide": "Show / Hide",

        # File Monitor Status
        "status_no_file": "No monitored file specified",
        "status_file_not_found": "File not found: {filename}",
        "status_monitoring": "Monitoring: {filename}",
        "status_read_error": "Read error: {error}",

        # Mode Dialog
        "mode_dlg_title": "Recording Mode",
        "mode_dlg_header_title": "Geometry Recording Mode",
        "mode_dlg_header_sub": "How Abaqus records geometric objects in .rpy",
        "mode_dlg_guide_btn": "Guide",
        "mode_dlg_sec_mode": "Mode",
        "mode_dlg_sec_session": "Current Session",
        "mode_dlg_copy_inject_btn": " Copy command & focus Abaqus",
        "mode_dlg_sec_startup": "Startup Default",
        "mode_dlg_write_btn": " Write",
        "mode_dlg_clear_btn": " Clear",
        "mode_dlg_open_folder_btn": " Open Folder",
        "mode_dlg_close_btn": "Close",
        "mode_dlg_abq_running": "● Abaqus/CAE is running",
        "mode_dlg_abq_process_running": "● Abaqus process running (window not found)",
        "mode_dlg_abq_not_running": "○ Abaqus/CAE not detected",
        "mode_dlg_env_configured": "{path}\nConfigured: {mode}",
        "mode_dlg_env_not_configured": "{path}\nNot configured",
        "mode_dlg_copied_title": "Copied",
        "mode_dlg_copied_body": "{command}\n\nPaste and press Enter in the Abaqus/CAE command line (>>>) to apply.",
        "mode_dlg_saved_title": "Saved",
        "mode_dlg_saved_body": "{msg}\n\nAbaqus/CAE will automatically use {badge} mode on next startup.",
        "mode_dlg_save_failed_title": "Write Failed",
        "mode_dlg_cleared_title": "Cleared",
        "mode_dlg_clear_failed_title": "Clear Failed",
        "env_file_not_found": "Configuration file does not exist",
        "env_write_ok": "Written to:\n{path}",
        "env_write_failed": "Write failed: {error}",
        "env_file_deleted": "Deleted:\n{path}",
        "env_file_cleared": "Cleared:\n{path}",
        "env_file_clear_failed": "Clear failed: {error}",

        # Guide Dialog
        "guide_dlg_title": "Recording Mode Guide",
        "guide_dlg_close_btn": "Close",

        # Mode Details
        "mode_coord_title": "Coordinate (COORDINATE)",
        "mode_coord_badge": "Coordinate",
        "mode_coord_tag": "Recommended",
        "mode_coord_desc": "findAt((x, y, z)), remains valid after model geometry changes; ideal for parametric modeling.",

        "mode_index_title": "Index (INDEX)",
        "mode_index_badge": "Index",
        "mode_index_tag": "",
        "mode_index_desc": "e[0], c[0:5]; ideal for iterating over elements and nodes.",

        "mode_compressed_title": "Mask (COMPRESSEDINDEX)",
        "mode_compressed_badge": "Mask",
        "mode_compressed_tag": "Default",
        "mode_compressed_desc": "getSequenceFromMask; invalid after geometry or mesh changes.",
    },
    "zh": {
        # App / Window
        "app_title": "AbaqusPythonReader",
        "no_file_selected": "未选择文件",
        "btn_file_tooltip": "更换监控文件",

        # Badges & Buttons
        "btn_mask_warning": "掩码",
        "btn_mask_warning_tooltip": "检测到 getSequenceFromMask，建议切换为坐标或索引模式",
        "btn_filter": "过滤",
        "btn_filter_tooltip": "隐藏视图操作（平移、旋转、缩放）",
        "btn_copy": "复制",
        "btn_copy_tooltip": "复制代码（不含视图操作）",
        "btn_copy_done": "已复制",
        "btn_pin_tooltip": "置顶",
        "btn_theme_tooltip": "切换主题",
        "btn_more_tooltip": "更多",
        "btn_minimize_tooltip": "最小化",
        "btn_close_tooltip": "退出",

        # Menu Actions
        "menu_copy": "复制",
        "menu_clear": "清空",
        "menu_open_file": "打开文件...",
        "menu_save_as": "另存为...",
        "menu_hide_viewport": "隐藏视图操作",
        "menu_word_wrap": "自动换行",
        "menu_auto_scroll": "自动滚动",
        "menu_line_numbers": "行号",
        "menu_hover_doc": "函数用法悬停提示",
        "menu_frameless": "无边框",
        "menu_opacity": "透明度",
        "menu_recording_mode": "录制模式",
        "menu_language": "语言",
        "menu_reset_window": "重置窗口位置",
        "menu_about": "关于",
        "menu_quit": "退出",

        # Mode Menu & Actions
        "mode_set_default": "设为启动默认...",
        "mode_guide": "录制模式说明",
        "mode_copied_toast": "已复制{badge}指令，在 Abaqus 命令行粘贴并回车",
        "mode_tooltip_cmd": "复制指令：{cmd}",

        # Toasts
        "toast_filter_hidden": "已隐藏视图操作",
        "toast_filter_shown": "已显示全部命令",
        "toast_cleared": "已清空",
        "toast_pinned": "已置顶",
        "toast_unpinned": "已取消置顶",
        "toast_word_wrap": "自动换行：{state}",
        "toast_auto_scroll": "自动滚动：{state}",
        "toast_line_numbers": "行号：{state}",
        "toast_hover_doc": "函数用法提示：{state}",
        "toast_frameless": "无边框：{state}",
        "toast_opacity": "透明度 {percent}%",
        "toast_window_centered": "窗口已居中",
        "toast_saved": "已保存 {filename}",
        "toast_lang_changed": "已切换为简体中文",
        "state_on": "开",
        "state_off": "关",

        # File Dialogs & Errors
        "dlg_open_title": "打开监控文件",
        "dlg_open_filter": "Abaqus 脚本 (*.rpy *.jnl *.py);;所有文件 (*.*)",
        "dlg_save_title": "另存为",
        "dlg_save_filter": "Python 脚本 (*.py);;文本文件 (*.txt);;所有文件 (*.*)",
        "dlg_save_failed_title": "保存失败",

        # About Dialog
        "about_title": "关于",
        "about_desc": "Abaqus/CAE 命令流实时查看工具",
        "about_author": "基于焦博士（<a href='mailto:ck436@126.com'>ck436@126.com</a>）2010 年开发的 ABAQUS-PythonReader 重写。<br>API 接口文档来源于 <a href='https://github.com/haiiliin/abqpy'>abqpy</a>（Hailin Wang）。",
        "about_license": "MIT License",

        # Tray Menu
        "tray_show_hide": "显示/隐藏",

        # File Monitor Status
        "status_no_file": "未指定监控文件",
        "status_file_not_found": "文件未找到: {filename}",
        "status_monitoring": "监控中: {filename}",
        "status_read_error": "读取错误: {error}",

        # Mode Dialog
        "mode_dlg_title": "录制模式",
        "mode_dlg_header_title": "几何录制模式",
        "mode_dlg_header_sub": "Abaqus 在 .rpy 中记录几何对象的方式",
        "mode_dlg_guide_btn": "说明",
        "mode_dlg_sec_mode": "模式",
        "mode_dlg_sec_session": "当前会话",
        "mode_dlg_copy_inject_btn": " 复制指令并切换到 Abaqus",
        "mode_dlg_sec_startup": "启动默认",
        "mode_dlg_write_btn": " 写入",
        "mode_dlg_clear_btn": " 清除",
        "mode_dlg_open_folder_btn": " 打开目录",
        "mode_dlg_close_btn": "关闭",
        "mode_dlg_abq_running": "● Abaqus/CAE 已运行",
        "mode_dlg_abq_process_running": "● Abaqus 进程运行中（未找到窗口）",
        "mode_dlg_abq_not_running": "○ 未检测到 Abaqus/CAE",
        "mode_dlg_env_configured": "{path}\n已设置：{mode}",
        "mode_dlg_env_not_configured": "{path}\n未设置",
        "mode_dlg_copied_title": "已复制",
        "mode_dlg_copied_body": "{command}\n\n在 Abaqus/CAE 命令行（>>>）中粘贴并回车即可生效。",
        "mode_dlg_saved_title": "已写入",
        "mode_dlg_saved_body": "{msg}\n\n之后启动 Abaqus/CAE 时自动使用{badge}模式。",
        "mode_dlg_save_failed_title": "写入失败",
        "mode_dlg_cleared_title": "已清除",
        "mode_dlg_clear_failed_title": "清除失败",
        "env_file_not_found": "配置文件不存在",
        "env_write_ok": "已写入：\n{path}",
        "env_write_failed": "写入失败：{error}",
        "env_file_deleted": "已删除：\n{path}",
        "env_file_cleared": "已清除：\n{path}",
        "env_file_clear_failed": "清除失败：{error}",

        # Guide Dialog
        "guide_dlg_title": "录制模式说明",
        "guide_dlg_close_btn": "关闭",

        # Mode Details
        "mode_coord_title": "坐标（COORDINATE）",
        "mode_coord_badge": "坐标",
        "mode_coord_tag": "推荐",
        "mode_coord_desc": "findAt((x, y, z))，模型修改后仍可用，适合参数化建模。",

        "mode_index_title": "索引（INDEX）",
        "mode_index_badge": "索引",
        "mode_index_tag": "",
        "mode_index_desc": "e[0]、c[0:5]，适合遍历单元和节点。",

        "mode_compressed_title": "掩码（COMPRESSEDINDEX）",
        "mode_compressed_badge": "掩码",
        "mode_compressed_tag": "默认",
        "mode_compressed_desc": "getSequenceFromMask，模型修改后失效。",
    },
}


def tr(key: str, lang: Optional[str] = None, **kwargs) -> str:
    """Translates a message key to the target language (defaulting to current language)."""
    selected_lang = lang or _current_language
    text = TRANSLATIONS.get(selected_lang, {}).get(key)
    if text is None:
        # Fallback to English, then to key itself
        text = TRANSLATIONS.get(DEFAULT_LANGUAGE, {}).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def get_guide_html(lang: Optional[str] = None) -> str:
    """Returns HTML content for the Abaqus recording mode guide dialog."""
    selected_lang = lang or _current_language
    if selected_lang == "zh":
        return """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", sans-serif; font-size: 13px; line-height: 1.6; color: #1e293b; }
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
</html>"""
    else:
        return """<!DOCTYPE html>
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
    <p>By default, Abaqus/CAE records selected geometry using masks (<code>getSequenceFromMask</code>).
    Masks rely on internal entity numbering and will select incorrect entities or fail after geometry modifications or remeshing. Coordinate mode is recommended for scripting.</p>
    <table>
        <tr><th>Mode</th><th>Example</th><th>Use Case</th></tr>
        <tr><td>Coordinate</td><td><code>findAt(((x, y, z), ))</code></td><td>Parametric modeling</td></tr>
        <tr><td>Index</td><td><code>p.elements[0:10]</code></td><td>Iterating elements and nodes</td></tr>
        <tr><td>Mask</td><td><code>getSequenceFromMask(...)</code></td><td>Abaqus default</td></tr>
    </table>
    <p>Switch manually in the Abaqus/CAE command line interface (CLI):</p>
    <pre>session.journalOptions.setValues(
    replayGeometry=COORDINATE, recoverGeometry=COORDINATE)</pre>
</body>
</html>"""
