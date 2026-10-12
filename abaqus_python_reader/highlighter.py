import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression
from .abaqus_docs import AbaqusDocManager

# Color palettes
THEMES = {
    "dark": {
        "background": "#1e1e2e",
        "editor_bg": "#181825",
        "text": "#cdd6f4",
        "keyword": "#cba6f7",       # Mauve
        "builtin": "#89b4fa",       # Blue
        "abaqus_api": "#f9e2af",    # Yellow
        "function": "#89dceb",      # Sky
        "string": "#a6e3a1",        # Green
        "number": "#fab387",        # Peach
        "comment": "#6c7086",       # Overlay0 (muted gray)
        "decorator": "#f5c2e7",     # Pink
        "operator": "#94e2d5",      # Teal
        "selection_bg": "#45475a",
        "line_number": "#585b70",
        "line_number_bg": "#11111b",
        "toolbar_bg": "#1e1e2e",
        "border": "#313244",
        "button_bg": "#313244",
        "button_hover": "#45475a",
        "type_hint_bg": "#1e3a5f",  # Deep navy badge background
        "type_hint_fg": "#7dd3fc",  # Sky light text
    },
    "light": {
        "background": "#ffffff",
        "editor_bg": "#ffffff",
        "text": "#1f2937",
        "keyword": "#7c3aed",
        "builtin": "#2563eb",
        "abaqus_api": "#b45309",
        "function": "#4338ca",
        "string": "#059669",
        "number": "#d97706",
        "comment": "#9ca3af",
        "decorator": "#db2777",
        "operator": "#4b5563",
        "selection_bg": "#e0e7ff",
        "line_number": "#9ca3af",
        "line_number_bg": "#f9fafb",
        "toolbar_bg": "#f9fafb",
        "border": "#e5e7eb",
        "button_bg": "#f3f4f6",
        "button_hover": "#e5e7eb",
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

        # Multi-line string delimiters
        self.tri_single_start = QRegularExpression(r"'''")
        self.tri_single_end = QRegularExpression(r"'''")
        self.tri_double_start = QRegularExpression(r'"""')
        self.tri_double_end = QRegularExpression(r'"""')

    def highlightBlock(self, text):
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
