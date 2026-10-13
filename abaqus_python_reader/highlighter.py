import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression
from .abaqus_docs import AbaqusDocManager

# Color palettes (Taste Skill: Linear/Raycast CAD/CAE HUD aesthetic)
THEMES = {
    "dark": {
        "background": "#0f172a",
        "editor_bg": "#0f172a",
        "text": "#f1f5f9",
        "keyword": "#c084fc",       # Purple
        "builtin": "#60a5fa",       # Blue
        "abaqus_api": "#fbbf24",    # Amber
        "function": "#38bdf8",      # Sky
        "string": "#4ade80",        # Green
        "number": "#fb923c",        # Orange
        "comment": "#64748b",       # Slate muted
        "decorator": "#f472b6",     # Pink
        "operator": "#2dd4bf",      # Teal
        "selection_bg": "#1e3a5f",  # Deep navy selection
        "line_number": "#64748b",
        "line_number_bg": "#0b1120",
        "toolbar_bg": "#1e293b",
        "border": "#334155",
        "button_bg": "#1e293b",
        "button_hover": "#334155",
        "type_hint_bg": "#1e3a5f",  # Deep navy badge background
        "type_hint_fg": "#7dd3fc",  # Sky light text
    },
    "light": {
        "background": "#ffffff",
        "editor_bg": "#ffffff",
        "text": "#0f172a",
        "keyword": "#7c3aed",
        "builtin": "#0284c7",
        "abaqus_api": "#d97706",
        "function": "#2563eb",
        "string": "#16a34a",
        "number": "#ea580c",
        "comment": "#94a3b8",
        "decorator": "#db2777",
        "operator": "#475569",
        "selection_bg": "#e0f2fe",
        "line_number": "#94a3b8",
        "line_number_bg": "#f8fafc",
        "toolbar_bg": "#f8fafc",
        "border": "#cbd5e1",
        "button_bg": "#f1f5f9",
        "button_hover": "#e2e8f0",
        "type_hint_bg": "#bae6fd",  # Sky-200 pastel blue background
        "type_hint_fg": "#0369a1",  # Deep sky blue text
    }
}

PYTHON_KEYWORDS = [
    "and", "as", "assert", "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally", "for", "from",
    "global", "if", "import", "in", "is", "lambda", "nonlocal", "not",
    "or", "pass", "raise", "return", "try", "while", "with", "yield",
    "True", "False", "None"
]

PYTHON_BUILTINS = [
    "abs", "all", "any", "bin", "bool", "bytearray", "bytes", "callable",
    "chr", "classmethod", "compile", "complex", "delattr", "dict", "dir",
    "divmod", "enumerate", "eval", "exec", "filter", "float", "format",
    "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex",
    "id", "input", "int", "isinstance", "issubclass", "iter", "len",
    "list", "locals", "map", "max", "memoryview", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "property", "range", "repr",
    "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod",
    "str", "sum", "super", "tuple", "type", "vars", "zip"
]

ABAQUS_KEYWORDS = [
    "mdb", "session", "odb", "part", "assembly", "step", "mesh",
    "material", "section", "interaction", "load", "boundaryCondition",
    "fieldOutput", "historyOutput", "job", "visualization", "xyPlot",
    "displayGroup", "annotation", "sketch", "datum", "feature",
    "Region", "Boolean", "Float", "Int", "String", "Symbol",
    "ON", "OFF", "DEFAULT", "COORDINATE", "INDEX", "ALL"
]


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document, theme_name="dark", type_hints_enabled=True):
        super().__init__(document)
        self.theme_name = theme_name
        self.type_hints_enabled = type_hints_enabled
        self.doc_manager = AbaqusDocManager.get_instance()
        self.ident_pattern = QRegularExpression(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
        self.highlighting_rules = []
        self.string_comment_rules = []
        self._init_rules()

    def set_theme(self, theme_name):
        self.theme_name = theme_name
        self._init_rules()
        self.rehighlight()

    def set_type_hints_enabled(self, enabled: bool):
        if self.type_hints_enabled != enabled:
            self.type_hints_enabled = enabled
            self.rehighlight()

    def _init_rules(self):
        self.highlighting_rules.clear()
        self.string_comment_rules.clear()
        colors = THEMES[self.theme_name]

        def create_format(color_hex, bold=False, italic=False):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color_hex))
            if bold:
                fmt.setFontWeight(QFont.Weight.Bold)
            if italic:
                fmt.setFontItalic(True)
            return fmt

        # Format styles
        keyword_fmt = create_format(colors["keyword"], bold=True)
        builtin_fmt = create_format(colors["builtin"])
        abaqus_fmt = create_format(colors["abaqus_api"], bold=True)
        function_fmt = create_format(colors["function"])
        number_fmt = create_format(colors["number"])
        decorator_fmt = create_format(colors["decorator"])
        self.comment_fmt = create_format(colors["comment"], italic=True)
        self.string_fmt = create_format(colors["string"])

        # Type hints badge format (functions/symbols with documentation)
        self.type_hint_fmt = QTextCharFormat()
        self.type_hint_fmt.setBackground(QColor(colors.get("type_hint_bg", "#1e3a5f")))
        self.type_hint_fmt.setForeground(QColor(colors.get("type_hint_fg", "#7dd3fc")))
        self.type_hint_fmt.setFontWeight(QFont.Weight.DemiBold)

        # 1. Keywords
        for kw in PYTHON_KEYWORDS:
            pattern = QRegularExpression(rf"\b{kw}\b")
            self.highlighting_rules.append((pattern, keyword_fmt))

        # 2. Builtins
        for bi in PYTHON_BUILTINS:
            pattern = QRegularExpression(rf"\b{bi}\b")
            self.highlighting_rules.append((pattern, builtin_fmt))

        # 3. Abaqus API namespaces
        for ab in ABAQUS_KEYWORDS:
            pattern = QRegularExpression(rf"\b{ab}\b")
            self.highlighting_rules.append((pattern, abaqus_fmt))

        # 4. Function definitions (def func_name)
        func_pattern = QRegularExpression(r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)")
        self.highlighting_rules.append((func_pattern, function_fmt))

        # 5. Class definitions (class ClassName)
        class_pattern = QRegularExpression(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)")
        self.highlighting_rules.append((class_pattern, function_fmt))

        # 6. Decorators (@decorator)
        dec_pattern = QRegularExpression(r"@[A-Za-z_][A-Za-z0-9_]*")
        self.highlighting_rules.append((dec_pattern, decorator_fmt))

        # 7. Numbers
        num_pattern = QRegularExpression(r"\b[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?\b")
        self.highlighting_rules.append((num_pattern, number_fmt))

        # 8. Single and Double Quoted Strings (single line)
        self.str_single = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.str_double = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.string_comment_rules.append((self.str_single, self.string_fmt))
        self.string_comment_rules.append((self.str_double, self.string_fmt))

        # 9. Single-line Comments (# ...)
        self.comment_pattern = QRegularExpression(r"#.*")
        self.string_comment_rules.append((self.comment_pattern, self.comment_fmt))

        # Block banner formatting
        is_dark = (self.theme_name == "dark")
        self.block_border_fmt = QTextCharFormat()
        self.block_border_fmt.setForeground(QColor("#475569" if is_dark else "#94a3b8"))
        self.block_border_fmt.setFontWeight(QFont.Weight.Bold)

        self.block_title_fmt = QTextCharFormat()
        self.block_title_fmt.setForeground(QColor("#38bdf8" if is_dark else "#0284c7"))
        self.block_title_fmt.setBackground(QColor(56, 189, 248, 30) if is_dark else QColor(2, 132, 199, 22))
        self.block_title_fmt.setFontWeight(QFont.Weight.Bold)

        # Multi-line string delimiters
        self.tri_single_start = QRegularExpression(r"'''")
        self.tri_single_end = QRegularExpression(r"'''")
        self.tri_double_start = QRegularExpression(r'"""')
        self.tri_double_end = QRegularExpression(r'"""')

    def highlightBlock(self, text):
        stripped = text.strip()
        if stripped.startswith("# ==============================================================================") or \
           stripped.startswith("# ------------------------------------------------------------------------------"):
            self.setFormat(0, len(text), self.block_border_fmt)
            return
        elif stripped.startswith("# 【功能分区】") or stripped.startswith("# [Block]") or stripped.startswith("# [Stage:"):
            self.setFormat(0, len(text), self.block_title_fmt)
            return

        # 1. Base syntax highlighting (keywords, builtins, numbers, defs)
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # 2. Highlight symbols with Type Hints using distinct background color
        if self.type_hints_enabled:
            match_iterator = self.ident_pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                word = match.captured()
                if self.doc_manager.has_symbol(word):
                    self.setFormat(match.capturedStart(), match.capturedLength(), self.type_hint_fmt)

        # 3. Apply strings and comments (override type hint badge inside strings/comments)
        for pattern, fmt in self.string_comment_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # 4. Multi-line strings (triple quotes)
        self.setCurrentBlockState(0)
        self._highlight_multiline(text, self.tri_double_start, self.tri_double_end, 1)
        self._highlight_multiline(text, self.tri_single_start, self.tri_single_end, 2)

    def _highlight_multiline(self, text, start_exp, end_exp, in_state):
        start_index = 0
        if self.previousBlockState() == in_state:
            start_index = 0
        else:
            match = start_exp.match(text)
            start_index = match.capturedStart() if match.hasMatch() else -1

        while start_index >= 0:
            match = end_exp.match(text, start_index + 3)
            end_index = match.capturedStart() if match.hasMatch() else -1
            comment_len = 0
            if end_index == -1:
                self.setCurrentBlockState(in_state)
                comment_len = len(text) - start_index
            else:
                comment_len = end_index - start_index + 3

            self.setFormat(start_index, comment_len, self.string_fmt)
            start_match = start_exp.match(text, start_index + comment_len)
            start_index = start_match.capturedStart() if start_match.hasMatch() else -1
