# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

AbaqusPythonReader is a Windows-only PySide6 (Qt6) HUD app that tails an Abaqus CAE replay journal (`abaqus.rpy`) in real time, syntax-highlights it, and optionally strips viewport noise (pan/rotate/zoom/fitView). It is a rewrite of a 2010 C# WinForms tool archived under `legacy/` (reference only — not built or tested). User-facing strings, docs and README are in Chinese.

UI text conventions (the maintainer explicitly wants a terse, professional tone):
- Menu items and buttons name the action only (`自动换行`, `重置窗口位置`) — no parenthetical explanations, marketing words (一键/强烈推荐/极致), exclamation marks or emoji. Put details in tooltips.
- Prefer a short toast (`show_toast`) over a modal `QMessageBox` for success feedback; keep message boxes for errors.
- Menu on/off items keep their function icon on the left; when on, `ToggleMenu` (app.py) paints the Lucide `SVG_CHECK` icon right-aligned (use `ToggleMenu.add_toggle`). Don't use checkable `QAction`s (Qt's Windows styles replace the icon with the check) or text glyphs like ✓ (don't match the Lucide icon set). Both the "more" button and right-click menu are built by `MainWindow._build_menu`.
- Copy and Save-as always strip viewport statements regardless of the filter toggle; this is intentional.

## Commands

```bash
pip install -r requirements-dev.txt          # runtime (PySide6) + pytest, pyinstaller, pillow
python run.py                                # launch the app (run.bat uses .venv\Scripts\pythonw.exe if present)
python -m unittest discover tests            # what CI runs (Windows, Python 3.10/3.11/3.12)
pytest                                       # also works; testpaths configured in pyproject.toml
pytest tests/test_cleaner.py::TestAbaqusCleaner::test_has_mask_statement   # single test
python -m unittest tests.test_cleaner.TestAbaqusCleaner.test_has_mask_statement   # same, without pytest
pyinstaller AbaqusPythonReader.spec          # one-file windowed exe -> dist/AbaqusPythonReader.exe
python scripts/build_icons.py                # regenerate app.ico + resources/icon_256.png from SVG_APP_LOGO
```

There is no linter/formatter configured. Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds the exe and attaches it to a GitHub release.

## Architecture

Data flow: `FileMonitor` → `MainWindow.raw_text_buffer` → `cleaner.clean_abaqus_script` → `CodeEditor` (+ `PythonHighlighter`).

- **`file_monitor.py`** — `QObject` polling via `QTimer` (250 ms default) rather than file-system watchers, so it never holds a lock that conflicts with Abaqus writing the journal. Tracks `last_pos`/`last_mtime`, reads only the appended tail and emits `new_content_appended(str)`. A shrinking file (new Abaqus session) emits `file_reset`. Falls back from UTF-8 to GBK on read errors.
- **`app.py`** — `MainWindow` owns everything: the frameless/topmost/translucent HUD, right-button drag-to-move, edge-resize via `_get_edge_at`, tray icon, toasts, menus, and all theme stylesheets (`_apply_theme_style`). On every new chunk it appends to `raw_text_buffer` and **re-cleans and re-renders the whole buffer** (`_refresh_editor_content`), so filtering is always applied to full text, not chunks. Also shows a warning button when `getSequenceFromMask` appears (mask-mode journals).
- **`cleaner.py`** — pure functions, no Qt. `split_python_statements` is a hand-written tokenizer tracking paren/bracket/brace depth and string/triple-quote state so multi-line calls are treated as one statement; `VIEWPORT_REGEX` then drops whole statements. Add new viewport patterns to `VIEWPORT_KEYWORDS`.
- **`abaqus_mode.py`** — journal recording modes (COORDINATE / INDEX / COMPRESSEDINDEX) in `MODE_INFO`. Writes/removes an `onCaeStartup()` block in the user-level `~/abaqus_v6.env` only (project-level env files were intentionally dropped), delimited by `HEADER_MARKER`/`FOOTER_MARKER` so it can be replaced idempotently without touching user content. Uses `ctypes` Win32 calls to detect/activate the Abaqus window for copy-and-focus.
- **`highlighter.py`** — `THEMES` dict (`"dark"`/`"light"`) is the single source of editor colors, consumed by both `PythonHighlighter` and `CodeEditor` (line-number gutter). Includes an Abaqus API keyword list.
- **`icons.py`** — Lucide icons stored as inline SVG strings (`SVG_*` constants), recolored and rasterized at runtime via `render_svg_to_icon`/`render_svg_to_pixmap`. Add icons here rather than as files. The app logo `SVG_APP_LOGO` is duplicated in `resources/icon.svg`; after changing it, update both and run `scripts/build_icons.py` to regenerate the static `app.ico` (exe/taskbar) and `icon_256.png` (README).
- **`config.py`** — `ConfigManager` merges `DEFAULT_CONFIG` with `abaqus_python_reader/config.json`, saving on every `set()`. Note the JSON file lives inside the package directory and is tracked in git, so running the app locally modifies a tracked file — avoid committing those incidental changes. New settings must be added to `DEFAULT_CONFIG`.

`run.py` and `main.py` both insert the project root into `sys.path`, so the app runs from source without installation. Package data (`resources/`, `app.ico`, `config.json`) is declared in `pyproject.toml`; the PyInstaller spec lists its own `datas` separately — update both when adding bundled files.

## Testing notes

Tests use `unittest`. Anything touching Qt signals/timers (e.g. `FileMonitor`) needs a `QCoreApplication` instance (see `tests/test_file_monitor.py`), and tests call `_check_file()` directly instead of waiting on the timer. `ConfigManager` takes a `filepath` argument so tests use a temp file instead of the real `config.json`. `examples/sample_abaqus.rpy` is a realistic journal (with viewport ops) for manual testing of highlighting and filtering.
