from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QToolTip
from PySide6.QtGui import QPainter, QColor, QTextFormat, QFont, QTextCursor, QHelpEvent
from PySide6.QtCore import Qt, QRect, QSize, QEvent
from .highlighter import PythonHighlighter, THEMES
from .abaqus_docs import AbaqusDocManager


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None, theme_name="dark", show_line_numbers=True):
        super().__init__(parent)
        self.theme_name = theme_name
        self.show_line_numbers = show_line_numbers
        self.auto_scroll = True
        self.hover_doc_enabled = True
        self.doc_manager = AbaqusDocManager.get_instance()

        self.line_number_area = LineNumberArea(self)
        self.highlighter = PythonHighlighter(self.document(), theme_name)

        # Editor configuration
        self.setReadOnly(True)
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)
        self.apply_theme(theme_name)

    def line_number_area_width(self):
        if not self.show_line_numbers:
            return 0
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        width = self.line_number_area_width()
        self.setViewportMargins(width, 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        if not self.show_line_numbers:
            return

        colors = THEMES[self.theme_name]
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(colors["line_number_bg"]))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        painter.setPen(QColor(colors["line_number"]))
        painter.setFont(self.font())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 8, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def apply_theme(self, theme_name):
        self.theme_name = theme_name
        self.highlighter.set_theme(theme_name)
        colors = THEMES[theme_name]

        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {colors["editor_bg"]};
                color: {colors["text"]};
                border: none;
                selection-background-color: {colors["selection_bg"]};
            }}
        """)
        self.line_number_area.update()

    def set_line_numbers_visible(self, visible: bool):
        self.show_line_numbers = visible
        self.update_line_number_area_width(0)
        self.line_number_area.setVisible(visible)

    def set_hover_doc_enabled(self, enabled: bool):
        self.hover_doc_enabled = enabled
        if not enabled:
            QToolTip.hideText()

    def viewportEvent(self, event):
        if event.type() == QEvent.Type.ToolTip and self.hover_doc_enabled:
            help_event: QHelpEvent = event
            pos = help_event.pos()
            cursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText().strip()

            if word and self.doc_manager.has_symbol(word):
                # Calculate bounding rect of the selected word
                start_cursor = QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())
                start_rect = self.cursorRect(start_cursor)

                end_cursor = QTextCursor(cursor)
                end_cursor.setPosition(cursor.selectionEnd())
                end_rect = self.cursorRect(end_cursor)

                word_rect = start_rect.united(end_rect)
                if word_rect.adjusted(-4, -4, 4, 4).contains(pos):
                    is_dark = (self.theme_name == "dark")
                    html_tip = self.doc_manager.format_tooltip_html(word, dark_theme=is_dark)
                    if html_tip:
                        QToolTip.showText(help_event.globalPos(), html_tip, self.viewport(), word_rect)
                        return True

            QToolTip.hideText()
            event.ignore()
            return True

        return super().viewportEvent(event)

    def scroll_to_bottom(self):
        if self.auto_scroll:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()

