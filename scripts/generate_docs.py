"""Extracts Abaqus Python API documentation from abqpy using AST.

Outputs:
    abaqus_python_reader/resources/abaqus_docs.json.gz

This script parses Python AST statically from the abqpy/abaqus package without
executing any Abaqus code or requiring runtime dependencies. The resulting
compressed JSON contains function/class signatures, docstrings, parameters,
constants, and access paths, enabling zero-latency hover tooltips in AbaqusPythonReader.

Usage:
    uv run --with abqpy python scripts/generate_docs.py
    # or:
    python scripts/generate_docs.py
"""
import os
import sys
import ast
import json
import gzip
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "abaqus_python_reader" / "resources" / "abaqus_docs.json.gz"


def get_annotation_str(node) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Attribute):
        val = get_annotation_str(node.value)
        return f"{val}.{node.attr}" if val else node.attr
    if isinstance(node, ast.Subscript):
        val = get_annotation_str(node.value)
        sl = get_annotation_str(node.slice)
        return f"{val}[{sl}]"
    if isinstance(node, ast.Tuple):
        return ", ".join(get_annotation_str(e) for e in node.elts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return f"{get_annotation_str(node.left)} | {get_annotation_str(node.right)}"
    return ""


def get_default_str(node) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        val = get_default_str(node.value)
        return f"{val}.{node.attr}" if val else node.attr
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return f"-{get_default_str(node.operand)}"
    return "..."


def parse_docstring_sections(docstring: str) -> dict:
    if not docstring:
        return {"summary": "", "access": "", "params": [], "returns": ""}

    # Extract access note
    access_match = re.search(r'can be accessed by::\s*\n\s*(?:import \w+\s*\n\s*)?([^\n]+)', docstring)
    access = access_match.group(1).strip() if access_match else ""

    # Split into sections based on reST / NumPy headers
    sections = re.split(r'\n(?=[A-Z][a-zA-Z\s]+\n[-=]+\n)', docstring)
    summary_raw = sections[0]

    # Clean summary (strip .. note:: and leading reST directives)
    summary_lines = []
    for line in summary_raw.split('\n'):
        stripped = line.strip()
        if stripped.startswith('..'):
            break
        if stripped:
            summary_lines.append(stripped)
    summary = " ".join(summary_lines).strip()

    params = []
    returns = ""

    for sec in sections[1:]:
        lines = sec.strip().split('\n')
        header = lines[0].strip().lower()
        if header.startswith('param'):
            current_param = None
            current_desc = []
            for line in lines[2:]:
                if not line.strip():
                    continue
                if not line.startswith(' ') and not line.startswith('\t'):
                    if current_param:
                        params.append({"name": current_param, "desc": " ".join(current_desc).strip()})
                    current_param = line.split(':')[0].strip()
                    current_desc = []
                else:
                    current_desc.append(line.strip())
            if current_param:
                params.append({"name": current_param, "desc": " ".join(current_desc).strip()})
        elif header.startswith('return'):
            returns = " ".join([l.strip() for l in lines[2:] if l.strip()])

    return {
        "summary": summary,
        "access": access,
        "params": params,
        "returns": returns
    }


def find_abaqus_dir() -> Path:
    try:
        import abqpy
        abqpy_dir = Path(abqpy.__file__).resolve().parent
        candidate = abqpy_dir.parent / "abaqus"
        if candidate.exists() and candidate.is_dir():
            return candidate
    except ImportError:
        pass

    for p in sys.path:
        cand = Path(p) / "abaqus"
        if cand.exists() and cand.is_dir() and (cand / "Part").exists():
            return cand

    raise RuntimeError("Could not find installed 'abaqus' package from abqpy.")


def score_entry(entry: dict) -> int:
    score = 0
    kind = entry.get("kind", "")
    if kind == "constant":
        return 5  # Lowest priority if there's a same-named class/function

    if "mdb.models" in entry.get("access", ""):
        score += 50
    elif "session.odbs" in entry.get("access", ""):
        score += 10

    if entry.get("signature", "").endswith("()"):
        score -= 20
    else:
        score += 30

    if entry.get("summary"):
        score += len(entry["summary"]) // 10
    score += len(entry.get("params", [])) * 10
    return score


def main():
    abaqus_dir = find_abaqus_dir()
    print(f"[*] Found Abaqus package at: {abaqus_dir}")

    docs_by_symbol = {}
    total_files = 0

    # 1. Parse constants from UtilityAndView/abaqusConstants.py
    const_file = abaqus_dir / "UtilityAndView" / "abaqusConstants.py"
    if const_file.exists():
        try:
            with open(const_file, "r", encoding="utf-8") as fp:
                const_tree = ast.parse(fp.read(), filename="abaqusConstants.py")
            for node in const_tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith("_"):
                            c_name = target.id
                            entry = {
                                "name": c_name,
                                "kind": "constant",
                                "parent": "abaqusConstants",
                                "access": f"from abaqusConstants import {c_name}",
                                "signature": f"{c_name}: SymbolicConstant",
                                "summary": f"Abaqus symbolic constant '{c_name}' from abaqusConstants.",
                                "params": [],
                                "returns": "",
                            }
                            docs_by_symbol.setdefault(c_name, []).append(entry)
        except Exception as e:
            print(f"[-] Warning parsing constants: {e}")

    # 2. Walk all files for classes and functions
    for root, _, files in os.walk(abaqus_dir):
        for f in files:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            total_files += 1
            filepath = os.path.join(root, f)
            try:
                with open(filepath, "r", encoding="utf-8") as fp:
                    tree = ast.parse(fp.read(), filename=f)
            except Exception:
                continue

            for top_node in tree.body:
                if isinstance(top_node, ast.ClassDef):
                    class_name = top_node.name
                    class_doc = ast.get_docstring(top_node) or ""
                    parsed_class = parse_docstring_sections(class_doc)

                    class_entry = {
                        "name": class_name,
                        "kind": "class",
                        "parent": "",
                        "access": parsed_class["access"],
                        "signature": f"class {class_name}",
                        "summary": parsed_class["summary"],
                        "params": parsed_class["params"],
                        "returns": parsed_class["returns"],
                    }
                    docs_by_symbol.setdefault(class_name, []).append(class_entry)

                    # Methods within class
                    for node in top_node.body:
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if node.name.startswith("_") and node.name != "__init__":
                                continue
                            func_name = node.name
                            func_doc = ast.get_docstring(node) or ""
                            parsed_func = parse_docstring_sections(func_doc)

                            args_list = []
                            defaults = [None] * (len(node.args.args) - len(node.args.defaults)) + list(node.args.defaults)
                            for arg, default in zip(node.args.args, defaults):
                                if arg.arg == "self":
                                    continue
                                param_str = arg.arg
                                ann = get_annotation_str(arg.annotation)
                                if ann:
                                    param_str += f": {ann}"
                                if default is not None:
                                    d_val = get_default_str(default)
                                    param_str += f" = {d_val}"
                                args_list.append(param_str)

                            if node.args.vararg:
                                args_list.append(f"*{node.args.vararg.arg}")
                            if node.args.kwarg:
                                args_list.append(f"**{node.args.kwarg.arg}")

                            ret_ann = get_annotation_str(node.returns)
                            ret_str = f" -> {ret_ann}" if ret_ann else ""

                            is_init = (func_name == "__init__")
                            target_name = class_name if is_init else func_name
                            sig = f"{target_name}({', '.join(args_list)}){ret_str}"

                            entry = {
                                "name": target_name,
                                "kind": "constructor" if is_init else "method",
                                "parent": class_name,
                                "access": parsed_func["access"] or parsed_class["access"],
                                "signature": sig,
                                "summary": parsed_func["summary"] or parsed_class["summary"],
                                "params": parsed_func["params"] or (parsed_class["params"] if is_init else []),
                                "returns": parsed_func["returns"] or (parsed_class["returns"] if is_init else ""),
                            }
                            docs_by_symbol.setdefault(target_name, []).append(entry)

                elif isinstance(top_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if top_node.name.startswith("_"):
                        continue
                    func_name = top_node.name
                    func_doc = ast.get_docstring(top_node) or ""
                    parsed_func = parse_docstring_sections(func_doc)

                    args_list = []
                    defaults = [None] * (len(top_node.args.args) - len(top_node.args.defaults)) + list(top_node.args.defaults)
                    for arg, default in zip(top_node.args.args, defaults):
                        param_str = arg.arg
                        ann = get_annotation_str(arg.annotation)
                        if ann:
                            param_str += f": {ann}"
                        if default is not None:
                            d_val = get_default_str(default)
                            param_str += f" = {d_val}"
                        args_list.append(param_str)

                    ret_ann = get_annotation_str(top_node.returns)
                    ret_str = f" -> {ret_ann}" if ret_ann else ""
                    sig = f"{func_name}({', '.join(args_list)}){ret_str}"

                    entry = {
                        "name": func_name,
                        "kind": "function",
                        "parent": "",
                        "access": parsed_func["access"],
                        "signature": sig,
                        "summary": parsed_func["summary"],
                        "params": parsed_func["params"],
                        "returns": parsed_func["returns"],
                    }
                    docs_by_symbol.setdefault(func_name, []).append(entry)

    print(f"[*] Parsed {total_files} files, found {len(docs_by_symbol)} unique symbol names.")

    final_db = {}
    for sym, entries in docs_by_symbol.items():
        valid = [e for e in entries if e.get("summary") or not e.get("signature", "").endswith("()")]
        if not valid:
            valid = entries
        valid.sort(key=score_entry, reverse=True)
        final_db[sym] = valid[:2]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    raw_data = json.dumps(final_db, ensure_ascii=False).encode("utf-8")
    compressed = gzip.compress(raw_data, compresslevel=9)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(compressed)

    print(f"[+] Successfully wrote {len(final_db)} symbols to: {OUTPUT_FILE}")
    print(f"[+] Raw size: {len(raw_data) / 1024 / 1024:.2f} MB -> Gzip size: {len(compressed) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
