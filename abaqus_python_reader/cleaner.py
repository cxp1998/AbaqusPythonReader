import re

# Viewport patterns to filter out
VIEWPORT_KEYWORDS = [
    r"session\.viewports\[.*?\]\.view\.setValues\(",
    r"session\.viewports\[.*?\]\.view\.rotate\(",
    r"session\.viewports\[.*?\]\.view\.pan\(",
    r"session\.viewports\[.*?\]\.view\.zoom\(",
    r"session\.viewports\[.*?\]\.view\.fitView\(",
    r"session\.viewports\[.*?\]\.view\.magnify\(",
    r"session\.viewports\[.*?\]\.setValues\(displayedObject=",
    r"session\.viewports\[.*?\]\.makeCurrent\(",
    r"session\.viewports\[.*?\]\.viewportAnnotationOptions\.setValues\(",
]

VIEWPORT_REGEX = re.compile("|".join(VIEWPORT_KEYWORDS), re.DOTALL)


def split_python_statements(text: str) -> list[str]:
    """
    Splits Python script text into top-level statements/blocks,
    preserving multi-line function calls with open parentheses.
    """
    lines = text.splitlines(keepends=True)
    statements = []
    current_statement = []
    paren_depth = 0
    bracket_depth = 0
    brace_depth = 0
    in_single_quote = False
    in_double_quote = False
    in_triple_single = False
    in_triple_double = False

    for line in lines:
        current_statement.append(line)
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            # Handle comments
            if not (in_single_quote or in_double_quote or in_triple_single or in_triple_double):
                if ch == '#':
                    break # Ignore rest of line
                elif ch == '(':
                    paren_depth += 1
                elif ch == ')':
                    paren_depth = max(0, paren_depth - 1)
                elif ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    bracket_depth = max(0, bracket_depth - 1)
                elif ch == '{':
                    brace_depth += 1
                elif ch == '}':
                    brace_depth = max(0, brace_depth - 1)
                elif line[i:i+3] == "'''":
                    in_triple_single = True
                    i += 2
                elif line[i:i+3] == '"""':
                    in_triple_double = True
                    i += 2
                elif ch == "'":
                    in_single_quote = True
                elif ch == '"':
                    in_double_quote = True
            else:
                if in_triple_single and line[i:i+3] == "'''":
                    in_triple_single = False
                    i += 2
                elif in_triple_double and line[i:i+3] == '"""':
                    in_triple_double = False
                    i += 2
                elif in_single_quote:
                    if ch == '\\':
                        i += 1
                    elif ch == "'":
                        in_single_quote = False
                elif in_double_quote:
                    if ch == '\\':
                        i += 1
                    elif ch == '"':
                        in_double_quote = False
            i += 1

        # If all brackets and quotes closed and not indented (or line ended)
        if paren_depth == 0 and bracket_depth == 0 and brace_depth == 0 and not (in_single_quote or in_double_quote or in_triple_single or in_triple_double):
            statements.append("".join(current_statement))
            current_statement = []

    if current_statement:
        statements.append("".join(current_statement))

    return statements


def is_viewport_statement(stmt: str) -> bool:
    """Checks whether a Python statement is a viewport manipulation statement."""
    clean_stmt = stmt.strip()
    if not clean_stmt or clean_stmt.startswith("#"):
        return False
    return bool(VIEWPORT_REGEX.search(stmt))


def clean_abaqus_script(raw_text: str, filter_viewport: bool = True) -> str:
    """
    Cleans abaqus script:
    - Filters out viewport pan/rotate/zoom/setValues statements if filter_viewport is True
    - Trims excess blank lines
    """
    if not filter_viewport:
        return raw_text

    statements = split_python_statements(raw_text)
    clean_statements = []

    for stmt in statements:
        if not is_viewport_statement(stmt):
            clean_statements.append(stmt)

    result = "".join(clean_statements)
    # Collapse multiple consecutive blank lines into at most two
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result


def has_mask_statement(text: str) -> bool:
    """Checks whether text contains getSequenceFromMask statements."""
    return "getSequenceFromMask" in text


def format_standalone_script(raw_text: str, add_chapters: bool = True) -> str:
    """
    Converts recorded Abaqus commands into a clean, standalone runnable Python script:
    - Filters out viewport pan/rotate/zoom operations
    - Injects clean milestone chapter banners if add_chapters is True
    - Ensures standard Abaqus CAE environment imports and startup hooks are present
    - Avoids duplicate imports if already present
    - Normalizes formatting
    """
    cleaned_body = clean_abaqus_script(raw_text, filter_viewport=True).strip()
    if add_chapters:
        from .abaqus_milestones import inject_milestone_chapters
        cleaned_body = inject_milestone_chapters(cleaned_body).strip()

    header_parts = []

    # 1. Encoding declaration
    if not re.search(r'#\s*-\*-\s*coding[:=]', cleaned_body):
        header_parts.append("# -*- coding: mbcs -*-")

    # 2. Standard Abaqus CAE imports
    needed_imports = []
    if not re.search(r'\bfrom\s+abaqus\s+import\b|\bimport\s+abaqus\b', cleaned_body):
        needed_imports.append("from abaqus import *")
    if not re.search(r'\bfrom\s+abaqusConstants\s+import\b|\bimport\s+abaqusConstants\b', cleaned_body):
        needed_imports.append("from abaqusConstants import *")
    if not re.search(r'\bfrom\s+caeModules\s+import\b|\bimport\s+caeModules\b', cleaned_body):
        needed_imports.append("from caeModules import *")
    if not re.search(r'\bexecuteOnCaeStartup\s*\(', cleaned_body):
        needed_imports.append("from driverUtils import executeOnCaeStartup\nexecuteOnCaeStartup()")

    if needed_imports:
        header_parts.extend(needed_imports)

    if header_parts:
        header_block = "\n".join(header_parts)
        if cleaned_body:
            result = f"{header_block}\n\n{cleaned_body}\n"
        else:
            result = f"{header_block}\n"
    else:
        result = f"{cleaned_body}\n" if cleaned_body else ""

    return result


