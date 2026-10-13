from typing import Optional, List
from PySide6.QtWidgets import (
    QPlainTextEdit, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextBrowser, QApplication, QToolTip, QLineEdit, QTextEdit,
    QScrollArea
)
from PySide6.QtGui import (
    QPainter, QColor, QTextFormat, QFont, QTextCursor, QHelpEvent,
    QGuiApplication, QPalette, QTextCharFormat, QTextDocument
)
from PySide6.QtCore import Qt, QRect, QSize, QEvent, QPoint
from .highlighter import PythonHighlighter, THEMES
from .abaqus_docs import AbaqusDocManager
from .icons import (
    render_svg_to_icon, render_svg_to_pixmap,
    SVG_SEARCH, SVG_CHEVRON_UP, SVG_CHEVRON_DOWN, SVG_CLOSE
)
from .i18n import tr



class SearchOverlay(QFrame):
    """Floating HUD search bar for in-editor search with real-time highlighting and navigation."""

    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self.code_editor = editor
        self.setObjectName("SearchOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(7, 3, 7, 3)
        layout.setSpacing(5)

        # Search icon
        self.icon_label = QLabel(self)
        self.icon_label.setFixedSize(14, 14)
        layout.addWidget(self.icon_label)

        # Search text input
        self.input_field = QLineEdit(self)
        self.input_field.setObjectName("SearchInput")
        self.input_field.setPlaceholderText(tr("search_placeholder"))
        self.input_field.textChanged.connect(self._on_query_changed)
        layout.addWidget(self.input_field, 1)

        # Case sensitivity button
        self.btn_case = QPushButton("Aa", self)
        self.btn_case.setObjectName("SearchBtnCase")
        self.btn_case.setCheckable(True)
        self.btn_case.setToolTip(tr("search_match_case_tooltip"))
        self.btn_case.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_case.toggled.connect(self._on_query_changed)
        layout.addWidget(self.btn_case)

        # Match count indicator
        self.count_label = QLabel(self)
        self.count_label.setObjectName("SearchCount")
        layout.addWidget(self.count_label)

        # Previous match button
        self.btn_prev = QPushButton(self)
        self.btn_prev.setObjectName("SearchNavBtn")
        self.btn_prev.setToolTip(tr("search_prev_tooltip"))
        self.btn_prev.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_prev.clicked.connect(self.code_editor.find_prev)
        layout.addWidget(self.btn_prev)

        # Next match button
        self.btn_next = QPushButton(self)
        self.btn_next.setObjectName("SearchNavBtn")
        self.btn_next.setToolTip(tr("search_next_tooltip"))
        self.btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_next.clicked.connect(self.code_editor.find_next)
        layout.addWidget(self.btn_next)

        # Close button
        self.btn_close = QPushButton("✕", self)
        self.btn_close.setObjectName("SearchCloseBtn")
        self.btn_close.setToolTip(tr("search_close_tooltip"))
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_close.clicked.connect(self.code_editor.close_search_overlay)
        layout.addWidget(self.btn_close)

        # Install event filter to capture Return, Esc, Up, Down
        self.input_field.installEventFilter(self)

    def _on_query_changed(self):
        self.code_editor.perform_search()

    def update_position(self):
        if not self.isVisible():
            return
        self.adjustSize()
        w = max(self.width(), 290)
        h = 32
        self.resize(w, h)
        right_margin = 16
        vbar = self.code_editor.verticalScrollBar()
        if vbar and vbar.isVisible():
            right_margin += vbar.width()
        x = max(8, self.code_editor.width() - w - right_margin)
        y = 6
        self.move(x, y)
        self.raise_()

    def apply_theme(self, is_dark: bool):
        bg = "#0f172a" if is_dark else "#ffffff"
        border = "#334155" if is_dark else "#cbd5e1"
        input_bg = "#1e293b" if is_dark else "#f8fafc"
        input_border = "#334155" if is_dark else "#cbd5e1"
        txt = "#f1f5f9" if is_dark else "#0f172a"
        sub_txt = "#94a3b8" if is_dark else "#64748b"
        btn_hover = "#334155" if is_dark else "#e2e8f0"
        accent = "#38bdf8" if is_dark else "#0284c7"
        active_bg = "#1e3a5f" if is_dark else "#e0f2fe"

        self.icon_label.setPixmap(render_svg_to_pixmap(SVG_SEARCH, color=sub_txt, size=13))
        self.btn_prev.setIcon(render_svg_to_icon(SVG_CHEVRON_UP, color=sub_txt, size=13))
        self.btn_next.setIcon(render_svg_to_icon(SVG_CHEVRON_DOWN, color=sub_txt, size=13))

        self.setStyleSheet(f"""
            #SearchOverlay {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 6px;
            }}
            QLineEdit#SearchInput {{
                background-color: {input_bg};
                color: {txt};
                border: 1px solid {input_border};
                border-radius: 4px;
                padding: 1px 6px;
                font-size: 11px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                min-width: 130px;
            }}
            QLineEdit#SearchInput:focus {{
                border-color: {accent};
            }}
            QLabel#SearchCount {{
                color: {sub_txt};
                font-size: 11px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                padding: 0 3px;
            }}
            QPushButton#SearchBtnCase {{
                background-color: transparent;
                color: {sub_txt};
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 1px 5px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton#SearchBtnCase:hover {{
                background-color: {btn_hover};
                color: {txt};
            }}
            QPushButton#SearchBtnCase:checked {{
                background-color: {active_bg};
                color: {accent};
                border: 1px solid {accent};
            }}
            QPushButton#SearchNavBtn, QPushButton#SearchCloseBtn {{
                background-color: transparent;
                color: {sub_txt};
                border: none;
                border-radius: 3px;
                width: 19px;
                height: 19px;
                font-size: 11px;
            }}
            QPushButton#SearchNavBtn:hover, QPushButton#SearchCloseBtn:hover {{
                background-color: {btn_hover};
                color: {txt};
            }}
            QPushButton#SearchCloseBtn:hover {{
                background-color: #ef4444;
                color: #ffffff;
            }}
        """)

    def eventFilter(self, obj, event):
        if obj == self.input_field and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.code_editor.close_search_overlay()
                return True
            elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    self.code_editor.find_prev()
                else:
                    self.code_editor.find_next()
                return True
            elif event.key() == Qt.Key.Key_Down:
                self.code_editor.find_next()
                return True
            elif event.key() == Qt.Key.Key_Up:
                self.code_editor.find_prev()
                return True
        return super().eventFilter(obj, event)


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

        self._search_matches: List[QTextCursor] = []
        self._current_match_idx: int = -1

        self.line_number_area = LineNumberArea(self)
        self.highlighter = PythonHighlighter(self.document(), theme_name, type_hints_enabled=True)
        self.type_hint_popup = TypeHintPopup(self)
        self.search_overlay = SearchOverlay(self)

        # Editor font configuration
        initial_font_size = 10
        if parent and hasattr(parent, "config"):
            initial_font_size = parent.config.get("font_size", 10)
        font = QFont("Consolas", initial_font_size)
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
        if hasattr(self, "search_overlay") and self.search_overlay.isVisible():
            self.search_overlay.update_position()

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
                block_str = block.text().strip()
                if block_str.startswith("# 【功能分区】") or block_str.startswith("# [Block]") or block_str.startswith("# [Stage:"):
                    accent_col = QColor("#38bdf8" if self.theme_name == "dark" else "#0284c7")
                    painter.fillRect(0, top, 3, bottom - top, accent_col)
                painter.drawText(0, top, self.line_number_area.width() - 8, self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def setPlainText(self, text: str):
        super().setPlainText(text)
        if hasattr(self, "search_overlay") and self.search_overlay.isVisible():
            self.perform_search()

    def jump_to_line(self, line_number: int):
        """Navigates editor to 1-indexed line_number, centers the line in view, and sets cursor."""
        doc = self.document()
        block = doc.findBlockByLineNumber(max(0, line_number - 1))
        if block.isValid():
            cursor = QTextCursor(block)
            self.setTextCursor(cursor)
            self.centerCursor()
            self.ensureCursorVisible()

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
        if hasattr(self, "search_overlay"):
            self.search_overlay.apply_theme(theme_name == "dark")
            if self._search_matches:
                self._update_search_extra_selections()



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

    # ------------------ Search & Highlight Navigation ------------------
    def open_search_overlay(self):
        """Opens or focuses the in-editor search overlay, pre-filling selected text if any."""
        tc = self.textCursor()
        sel = tc.selectedText().strip()
        if sel and "\u2029" not in sel:
            self.search_overlay.input_field.setText(sel)
        self.search_overlay.show()
        self.search_overlay.update_position()
        self.search_overlay.input_field.setFocus()
        self.search_overlay.input_field.selectAll()
        self.perform_search()

    def close_search_overlay(self):
        """Hides the search overlay, clears search highlights, and refocuses the editor."""
        self.search_overlay.hide()
        self._clear_search_highlight()
        self.setFocus()

    def _clear_search_highlight(self):
        self._search_matches.clear()
        self._current_match_idx = -1
        self.setExtraSelections([])

    def perform_search(self):
        """Finds all occurrences of current query, updates ExtraSelections and count label."""
        query = self.search_overlay.input_field.text()
        if not query:
            self._clear_search_highlight()
            self.search_overlay.count_label.setText("")
            return

        doc = self.document()
        find_flags = QTextDocument.FindFlag(0)
        if self.search_overlay.btn_case.isChecked():
            find_flags |= QTextDocument.FindFlag.FindCaseSensitively

        matches = []
        cursor = doc.find(query, 0, find_flags)
        while not cursor.isNull():
            matches.append(cursor)
            cursor = doc.find(query, cursor, find_flags)

        self._search_matches = matches
        if not matches:
            self._current_match_idx = -1
            self.search_overlay.count_label.setText(tr("search_no_results"))
            self._update_search_extra_selections()
            return

        # Jump to match closest to current cursor position
        curr_pos = self.textCursor().selectionStart()
        idx = 0
        for i, m in enumerate(matches):
            if m.selectionStart() >= curr_pos:
                idx = i
                break
        self._current_match_idx = idx
        self.search_overlay.count_label.setText(f"{idx + 1}/{len(matches)}")
        self._jump_to_match(idx)

    def find_next(self):
        """Jumps to the next search match."""
        if not self._search_matches:
            return
        self._current_match_idx = (self._current_match_idx + 1) % len(self._search_matches)
        self.search_overlay.count_label.setText(f"{self._current_match_idx + 1}/{len(self._search_matches)}")
        self._jump_to_match(self._current_match_idx)

    def find_prev(self):
        """Jumps to the previous search match."""
        if not self._search_matches:
            return
        self._current_match_idx = (self._current_match_idx - 1) % len(self._search_matches)
        self.search_overlay.count_label.setText(f"{self._current_match_idx + 1}/{len(self._search_matches)}")
        self._jump_to_match(self._current_match_idx)

    def _jump_to_match(self, idx: int):
        if 0 <= idx < len(self._search_matches):
            match_cursor = self._search_matches[idx]
            self.setTextCursor(match_cursor)
            self.ensureCursorVisible()
            self._update_search_extra_selections()

    def _update_search_extra_selections(self):
        is_dark = (self.theme_name == "dark")
        selections = []

        other_fmt = QTextCharFormat()
        other_bg = QColor("#854d0e" if is_dark else "#fef08a")
        other_fg = QColor("#fef08a" if is_dark else "#713f12")
        other_fmt.setBackground(other_bg)
        other_fmt.setForeground(other_fg)

        curr_fmt = QTextCharFormat()
        curr_bg = QColor("#38bdf8" if is_dark else "#0284c7")
        curr_fg = QColor("#0f172a" if is_dark else "#ffffff")
        curr_fmt.setBackground(curr_bg)
        curr_fmt.setForeground(curr_fg)
        curr_fmt.setFontWeight(QFont.Weight.Bold)

        for i, m in enumerate(self._search_matches):
            sel = QTextEdit.ExtraSelection()
            sel.cursor = m
            sel.format = curr_fmt if i == self._current_match_idx else other_fmt
            selections.append(sel)

        self.setExtraSelections(selections)

    # ------------------ Font Zooming (Ctrl+Wheel / Shortcuts) ------------------
    def zoom_font(self, delta_pt: int):
        """Zooms font size by delta_pt, clamping between 7pt and 24pt."""
        curr_size = self.font().pointSize()
        new_size = max(7, min(24, curr_size + delta_pt))
        if new_size != curr_size:
            f = self.font()
            f.setPointSize(new_size)
            self.setFont(f)
            self.update_line_number_area_width(0)
            parent_win = self.window()
            if hasattr(parent_win, "config"):
                parent_win.config.set("font_size", new_size)
            if hasattr(parent_win, "show_toast"):
                parent_win.show_toast(tr("toast_font_size", size=new_size), is_active=True, duration_ms=1000)

    def reset_font_zoom(self):
        """Resets font size to default 10pt."""
        default_size = 10
        f = self.font()
        if f.pointSize() != default_size:
            f.setPointSize(default_size)
            self.setFont(f)
            self.update_line_number_area_width(0)
            parent_win = self.window()
            if hasattr(parent_win, "config"):
                parent_win.config.set("font_size", default_size)
            if hasattr(parent_win, "show_toast"):
                parent_win.show_toast(tr("toast_font_size", size=default_size), is_active=True, duration_ms=1000)

    # ------------------ Wheel & Keyboard Event Overrides ------------------
    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_font(1)
            elif delta < 0:
                self.zoom_font(-1)
            event.accept()
            return
        super().wheelEvent(event)

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_F:
                self.open_search_overlay()
                event.accept()
                return
            elif event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
                self.zoom_font(1)
                event.accept()
                return
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_font(-1)
                event.accept()
                return
            elif event.key() == Qt.Key.Key_0:
                self.reset_font_zoom()
                event.accept()
                return
        elif event.key() == Qt.Key.Key_F3:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.find_prev()
            else:
                self.find_next()
            event.accept()
            return
        elif event.key() == Qt.Key.Key_Escape:
            if hasattr(self, "search_overlay") and self.search_overlay.isVisible():
                self.close_search_overlay()
                event.accept()
                return
        super().keyPressEvent(event)

