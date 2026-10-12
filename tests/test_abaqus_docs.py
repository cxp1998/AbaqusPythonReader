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


def test_editor_hover_event():
    import sys
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QHelpEvent
    from PySide6.QtCore import QEvent
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

    help_event = QHelpEvent(QEvent.Type.ToolTip, pos, editor.mapToGlobal(pos))
    handled = editor.viewportEvent(help_event)
    assert handled is True

    # Test disabled
    editor.set_hover_doc_enabled(False)
    assert editor.hover_doc_enabled is False

