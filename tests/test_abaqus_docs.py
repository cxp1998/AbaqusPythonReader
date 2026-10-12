import pytest
from abaqus_python_reader.abaqus_docs import AbaqusDocManager


def test_doc_manager_singleton():
    mgr1 = AbaqusDocManager.get_instance()
    mgr2 = AbaqusDocManager.get_instance()
    assert mgr1 is mgr2


def test_doc_manager_has_symbols():
    mgr = AbaqusDocManager.get_instance()
    assert mgr.has_symbol("BaseSolidExtrude")
    assert mgr.has_symbol("seedPart")
    assert mgr.has_symbol("StaticStep")
    assert mgr.has_symbol("Material")
    assert mgr.has_symbol("Elastic")
    assert mgr.has_symbol("THREE_D")
    assert not mgr.has_symbol("NonExistentAbaqusSymbol12345")


def test_doc_manager_get_doc():
    mgr = AbaqusDocManager.get_instance()
    docs = mgr.get_doc("BaseSolidExtrude")
    assert docs is not None
    assert len(docs) >= 1
    first = docs[0]
    assert first["name"] == "BaseSolidExtrude"
    assert "sketch" in first["signature"]
    assert "depth" in first["signature"]
    assert len(first["params"]) >= 2


def test_format_tooltip_html_dark_and_light():
    mgr = AbaqusDocManager.get_instance()
    
    html_dark = mgr.format_tooltip_html("BaseSolidExtrude", dark_theme=True)
    assert html_dark is not None
    assert "BaseSolidExtrude" in html_dark
    assert "sketch" in html_dark
    assert "#0f172a" in html_dark  # Dark bg
    assert "Parameters" in html_dark

    html_light = mgr.format_tooltip_html("BaseSolidExtrude", dark_theme=False)
    assert html_light is not None
    assert "BaseSolidExtrude" in html_light
    assert "#ffffff" in html_light  # Light bg


def test_format_tooltip_constant():
    mgr = AbaqusDocManager.get_instance()
    html_const = mgr.format_tooltip_html("THREE_D", dark_theme=True)
    assert html_const is not None
    assert "THREE_D" in html_const
    assert "SymbolicConstant" in html_const


def test_nonexistent_symbol_returns_none():
    mgr = AbaqusDocManager.get_instance()
    assert mgr.format_tooltip_html("definitely_not_an_abaqus_symbol_xyz") is None


def test_editor_click_and_cursor_events():
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QHelpEvent, QMouseEvent
    from PySide6.QtCore import QEvent, Qt, QPoint
    from abaqus_python_reader.editor import CodeEditor

    app = QApplication.instance() or QApplication(sys.argv)
    editor = CodeEditor(theme_name="dark")
    editor.setPlainText("p.BaseSolidExtrude(sketch=s, depth=25.0)")

    # Find position of BaseSolidExtrude
    text = editor.toPlainText()
    idx = text.find("BaseSolidExtrude")
    cursor = editor.textCursor()
    cursor.setPosition(idx + 3)
    pos = editor.cursorRect(cursor).center()

    # 1. Hover event does NOT show tooltip (hover tooltip is disabled)
    help_event = QHelpEvent(QEvent.Type.ToolTip, pos, editor.mapToGlobal(pos))
    handled = editor.viewportEvent(help_event)
    assert handled is True
    assert not editor.type_hint_popup.isVisible()

    # 2. Mouse move over type hint symbol sets PointingHandCursor
    move_event = QMouseEvent(
        QEvent.Type.MouseMove, pos, editor.mapToGlobal(pos),
        Qt.MouseButton.NoButton, Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier
    )
    editor.mouseMoveEvent(move_event)
    assert editor.viewport().cursor().shape() == Qt.CursorShape.PointingHandCursor

    # 3. Left-click on BaseSolidExtrude shows TypeHintPopup
    click_event = QMouseEvent(
        QEvent.Type.MouseButtonRelease, pos, editor.mapToGlobal(pos),
        Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier
    )
    editor.mouseReleaseEvent(click_event)
    assert editor.type_hint_popup.isVisible()
    assert editor.type_hint_popup._current_word == "BaseSolidExtrude"

    # 4. Clicking blank area dismisses popup
    blank_pos = QPoint(10, 100)
    blank_event = QMouseEvent(
        QEvent.Type.MouseButtonRelease, blank_pos, editor.mapToGlobal(blank_pos),
        Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier
    )
    editor.mouseReleaseEvent(blank_event)
    assert not editor.type_hint_popup.isVisible()

    # 5. Disable Type Hints
    editor.set_hover_doc_enabled(False)
    assert editor.hover_doc_enabled is False
    assert editor.highlighter.type_hints_enabled is False


def test_highlighter_type_hints_background():
    import sys
    from PySide6.QtWidgets import QApplication, QTextEdit
    from abaqus_python_reader.highlighter import PythonHighlighter, THEMES

    app = QApplication.instance() or QApplication(sys.argv)
    te = QTextEdit()
    hl = PythonHighlighter(te.document(), theme_name="dark", type_hints_enabled=True)

    # Verify colors exist in palettes
    assert "type_hint_bg" in THEMES["dark"]
    assert "type_hint_fg" in THEMES["dark"]
    assert "type_hint_bg" in THEMES["light"]
    assert "type_hint_fg" in THEMES["light"]

    # Verify type_hint_fmt has background color set
    assert hl.type_hint_fmt.background().color().isValid()
    assert hl.type_hint_fmt.background().color().name() == THEMES["dark"]["type_hint_bg"]

    # Test toggling
    hl.set_type_hints_enabled(False)
    assert hl.type_hints_enabled is False
    hl.set_type_hints_enabled(True)
    assert hl.type_hints_enabled is True

