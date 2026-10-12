from typing import Optional
from PySide6.QtWidgets import (
    QPlainTextEdit, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QApplication, QToolTip
)
from PySide6.QtGui import (
    QPainter, QColor, QTextFormat, QFont, QTextCursor, QHelpEvent, QGuiApplication, QPalette
)
from PySide6.QtCore import Qt, QRect, QSize, QEvent, QPoint
from .highlighter import PythonHighlighter, THEMES
from .abaqus_docs import AbaqusDocManager


class TypeHintPopup(QFrame):
    """Floating card displaying Abaqus API documentation and type hints on click."""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setAutoFillBackground(True)
        self.setObjectName("TypeHintPopup")
        self._filter_active = False
        self._current_word: Optional[str] = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header bar with title and close button
        self.header = QFrame(self)
        self.header.setObjectName("TypeHintHeader")
        self.header.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        h_layout = QHBoxLayout(self.header)
        h_layout.setContentsMargins(10, 4, 6, 4)
        h_layout.setSpacing(6)

        self.title_label = QLabel(self.header)
        font = QFont("Segoe UI", 9)
        font.setBold(True)
        self.title_label.setFont(font)
        h_layout.addWidget(self.title_label, 1)

        self.btn_close = QPushButton("✕", self.header)
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.clicked.connect(self.hide_doc)
        h_layout.addWidget(self.btn_close, 0)

        layout.addWidget(self.header)

        # Documentation content browser
        self.browser = QTextBrowser(self)
        self.browser.setReadOnly(True)
        self.browser.setOpenExternalLinks(True)
        self.browser.setFrameShape(QFrame.Shape.NoFrame)
        self.browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.browser)

    def show_doc(self, word: str, html_content: str, target_rect: QRect, viewport: QWidget, is_dark: bool = True):
        self._current_word = word
        self.title_label.setText(f"Type Hints: {word}")
        self.browser.setHtml(html_content)

        bg = "#0f172a" if is_dark else "#ffffff"
        border = "#334155" if is_dark else "#cbd5e1"
        hdr_bg = "#1e293b" if is_dark else "#f1f5f9"
        txt = "#f1f5f9" if is_dark else "#0f172a"
        title_col = "#38bdf8" if is_dark else "#0284c7"
        btn_hover = "#334155" if is_dark else "#e2e8f0"
        scroll_handle = "#475569" if is_dark else "#cbd5e1"

        pal = self.palette()
        pal.setColor(QPalette.ColorRole.Window, QColor(bg))
        self.setPalette(pal)

        self.setStyleSheet(f"""
            #TypeHintPopup {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            #TypeHintHeader {{
                background-color: {hdr_bg};
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                border-bottom: 1px solid {border};
            }}
            QLabel {{
                color: {title_col};
            }}
            QPushButton {{
                background: transparent;
                color: {txt};
                border: none;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {btn_hover};
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {scroll_handle};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        self.browser.setStyleSheet(f"background-color: {bg}; border: none;")

        # Size calculation
        self.browser.document().setTextWidth(420)
        doc_h = self.browser.document().size().height()
        w = 460
        h = int(min(max(doc_h + 38, 70), 380))
        self.resize(w, h)

        # Positioning: map word rect to global
        global_bottom_left = viewport.mapToGlobal(target_rect.bottomLeft())
        global_top_left = viewport.mapToGlobal(target_rect.topLeft())

        screen = QGuiApplication.screenAt(global_bottom_left) or QGuiApplication.primaryScreen()
        avail = screen.availableGeometry() if screen else QRect(0, 0, 1920, 1080)

        x = global_bottom_left.x()
        y = global_bottom_left.y() + 4

        # Flip above word if overflows bottom
        if y + h > avail.bottom() - 10:
            y = max(avail.top() + 10, global_top_left.y() - h - 4)

        # Clamp horizontal coordinates
        if x + w > avail.right() - 10:
            x = avail.right() - w - 10
        if x < avail.left() + 10:
            x = avail.left() + 10

        self.move(x, y)

        if not self._filter_active:
            app = QApplication.instance()
            if app:
                app.installEventFilter(self)
                self._filter_active = True

        self.show()

    def hide_doc(self):
        if self._filter_active:
            app = QApplication.instance()
            if app:
                app.removeEventFilter(self)
            self._filter_active = False
        self._current_word = None
        self.hide()

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.MouseButtonPress, QEvent.Type.NonClientAreaMouseButtonPress):
            global_pos = getattr(event, "globalPosition", None)
            if global_pos:
                pt = global_pos().toPoint() if callable(global_pos) else global_pos.toPoint()
            else:
                pt = getattr(event, "globalPos", lambda: QPoint())()
            if not self.geometry().contains(pt):
                self.hide_doc()
        elif event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.hide_doc()
            return True
        return super().eventFilter(obj, event)


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
        self.highlighter = PythonHighlighter(self.document(), theme_name, type_hints_enabled=True)
        self.type_hint_popup = TypeHintPopup(self)

        # Editor configuration
        self.setReadOnly(True)
        font = QFont("Consolas", 10)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        # Enable mouse tracking for interactive cursor changes on type-hint symbols
        self.viewport().setMouseTracking(True)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        # Dismiss popup on scroll
        self.verticalScrollBar().valueChanged.connect(self.hide_type_hint_popup)
        self.horizontalScrollBar().valueChanged.connect(self.hide_type_hint_popup)

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
        if self.type_hint_popup.isVisible():
            self.hide_type_hint_popup()

    def set_line_numbers_visible(self, visible: bool):
        self.show_line_numbers = visible
        self.update_line_number_area_width(0)
        self.line_number_area.setVisible(visible)

    def set_hover_doc_enabled(self, enabled: bool):
        """Toggles Type Hints background highlighting and click-to-view documentation."""
        self.hover_doc_enabled = enabled
        self.highlighter.set_type_hints_enabled(enabled)
        if not enabled:
            self.hide_type_hint_popup()
            self.viewport().setCursor(Qt.CursorShape.IBeamCursor)

    def hide_type_hint_popup(self):
        if self.type_hint_popup.isVisible():
            self.type_hint_popup.hide_doc()

    def show_type_hint_popup(self, word: str, target_rect: QRect):
        if not self.hover_doc_enabled:
            return
        is_dark = (self.theme_name == "dark")
        html_tip = self.doc_manager.format_tooltip_html(word, dark_theme=is_dark)
        if html_tip:
            self.type_hint_popup.show_doc(word, html_tip, target_rect, self.viewport(), is_dark=is_dark)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.hover_doc_enabled and event.buttons() == Qt.MouseButton.NoButton:
            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            cursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText().strip()
            if word and self.doc_manager.has_symbol(word):
                self.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
                return
        self.viewport().setCursor(Qt.CursorShape.IBeamCursor)

    def leaveEvent(self, event):
        self.viewport().setCursor(Qt.CursorShape.IBeamCursor)
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.MouseButton.LeftButton and self.hover_doc_enabled:
            # If user dragged and selected text across words, don't show popup
            tc = self.textCursor()
            if tc.hasSelection() and len(tc.selectedText().strip().split()) > 1:
                return

            pos = event.position().toPoint() if hasattr(event, "position") else event.pos()
            cursor = self.cursorForPosition(pos)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            word = cursor.selectedText().strip()

            if word and self.doc_manager.has_symbol(word):
                start_cursor = QTextCursor(cursor)
                start_cursor.setPosition(cursor.selectionStart())
                start_rect = self.cursorRect(start_cursor)

                end_cursor = QTextCursor(cursor)
                end_cursor.setPosition(cursor.selectionEnd())
                end_rect = self.cursorRect(end_cursor)

                word_rect = start_rect.united(end_rect)
                if self.type_hint_popup.isVisible() and self.type_hint_popup._current_word == word:
                    self.hide_type_hint_popup()
                else:
                    self.show_type_hint_popup(word, word_rect)
            else:
                self.hide_type_hint_popup()

    def viewportEvent(self, event):
        # Ignore hover tooltip events completely; type hints are displayed on click
        if event.type() == QEvent.Type.ToolTip:
            event.ignore()
            return True
        return super().viewportEvent(event)

    def scroll_to_bottom(self):
        if self.auto_scroll:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self.setTextCursor(cursor)
            self.ensureCursorVisible()
