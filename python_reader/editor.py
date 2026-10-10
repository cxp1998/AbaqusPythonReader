from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtGui import QPainter, QColor, QTextFormat, QFont, QTextCursor
from PySide6.QtCore import Qt, QRect, QSize
from .highlighter import PythonHighlighter, THEMES


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

    def scroll_to_bottom(self):
        if self.auto_scroll:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
