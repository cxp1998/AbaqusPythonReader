"""Abaqus Python API documentation provider and hover tooltip formatter.

Loads symbol documentation extracted from abqpy (compressed JSON) and
renders styled HTML tooltips for the code editor.
"""
import gzip
try:
    import html
except ImportError:
    # Fallback in case html module is excluded or unavailable in minimal runtime
    class _HtmlFallback:
        @staticmethod
        def escape(s: str, quote: bool = True) -> str:
            s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            if quote:
                s = s.replace('"', "&quot;").replace("'", "&#x27;")
            return s
    html = _HtmlFallback()
import json
from pathlib import Path
from typing import Optional, List, Dict, Any


DOCS_PATH = Path(__file__).resolve().parent / "resources" / "abaqus_docs.json.gz"


class AbaqusDocManager:
    """Manages the in-memory Abaqus documentation database."""
    _instance: Optional["AbaqusDocManager"] = None

    def __init__(self, db_path: Path = DOCS_PATH):
        self.db_path = db_path
        self._db: Optional[Dict[str, List[Dict[str, Any]]]] = None

    @classmethod
    def get_instance(cls) -> "AbaqusDocManager":
        if cls._instance is None:
            cls._instance = AbaqusDocManager()
        return cls._instance

    def _ensure_loaded(self):
        if self._db is not None:
            return
        if not self.db_path.exists():
            self._db = {}
            return
        try:
            with gzip.open(self.db_path, "rt", encoding="utf-8") as f:
                self._db = json.load(f)
        except Exception:
            self._db = {}

    def get_doc(self, symbol_name: str) -> Optional[List[Dict[str, Any]]]:
        """Returns documentation entries for the given symbol name, or None."""
        self._ensure_loaded()
        if not self._db:
            return None
        return self._db.get(symbol_name)

    def has_symbol(self, symbol_name: str) -> bool:
        self._ensure_loaded()
        return bool(self._db and symbol_name in self._db)

    def format_tooltip_html(
        self,
        symbol_name: str,
        dark_theme: bool = False,
        max_params: int = 8,
    ) -> Optional[str]:
        """Formats documentation for a symbol as a self-contained styled HTML tooltip."""
        entries = self.get_doc(symbol_name)
        if not entries:
            return None

        entry = entries[0]
        name = entry.get("name", symbol_name)
        kind = entry.get("kind", "function")
        parent = entry.get("parent", "")
        access = entry.get("access", "")
        signature = entry.get("signature", "")
        summary = entry.get("summary", "")
        params = entry.get("params", [])
        returns = entry.get("returns", "")

        # Theme colors
        if dark_theme:
            bg_card = "#0f172a"
            border_card = "#334155"
            header_bg = "#1e293b"
            sig_color = "#38bdf8"
            kind_badge_bg = "#0369a1"
            kind_badge_fg = "#e0f2fe"
            meta_color = "#94a3b8"
            summary_color = "#f1f5f9"
            section_title = "#cbd5e1"
            param_name_color = "#7dd3fc"
            param_desc_color = "#94a3b8"
            sep_color = "#1e293b"
        else:
            bg_card = "#ffffff"
            border_card = "#cbd5e1"
            header_bg = "#f8fafc"
            sig_color = "#0284c7"
            kind_badge_bg = "#e0f2fe"
            kind_badge_fg = "#0369a1"
            meta_color = "#64748b"
            summary_color = "#0f172a"
            section_title = "#334155"
            param_name_color = "#0369a1"
            param_desc_color = "#475569"
            sep_color = "#e2e8f0"

        # Badge text
        kind_label = kind.capitalize()
        if parent:
            kind_label += f" of {parent}"

        # Signature display
        sig_text = signature if signature else name

        html_parts = [
            f'<div style="background-color: {bg_card}; color: {summary_color}; '
            f'border: 1px solid {border_card}; border-radius: 6px; padding: 10px; '
            f'font-family: \'Segoe UI\', -apple-system, sans-serif; max-width: 480px; line-height: 1.45;">'
        ]

        # Header bar with badge and signature
        html_parts.append(
            f'<div style="background-color: {header_bg}; border: 1px solid {border_card}; '
            f'border-radius: 4px; padding: 6px 8px; margin-bottom: 8px;">'
            f'<div style="margin-bottom: 4px;">'
            f'<span style="background-color: {kind_badge_bg}; color: {kind_badge_fg}; '
            f'font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 3px;">'
            f'{html.escape(kind_label)}</span>'
            f'</div>'
            f'<div style="font-family: Consolas, monospace; font-size: 11px; '
            f'font-weight: 600; color: {sig_color}; word-break: break-all;">'
            f'{html.escape(sig_text)}'
            f'</div>'
            f'</div>'
        )

        # Access path if available
        if access:
            html_parts.append(
                f'<div style="font-size: 11px; color: {meta_color}; margin-bottom: 6px;">'
                f'<b>Access:</b> <code style="font-family: Consolas, monospace;">{html.escape(access)}</code>'
                f'</div>'
            )

        # Summary text
        if summary:
            html_parts.append(
                f'<div style="font-size: 12px; color: {summary_color}; margin-bottom: 8px;">'
                f'{html.escape(summary)}'
                f'</div>'
            )

        # Parameters section
        if params:
            html_parts.append(
                f'<div style="border-top: 1px solid {sep_color}; padding-top: 6px; margin-top: 6px;">'
                f'<div style="font-size: 11px; font-weight: 700; color: {section_title}; margin-bottom: 4px;">'
                f'Parameters'
                f'</div>'
            )
            displayed_params = params[:max_params]
            for p in displayed_params:
                p_name = p.get("name", "")
                p_desc = p.get("desc", "")
                html_parts.append(
                    f'<div style="font-size: 11px; margin-bottom: 4px; padding-left: 6px;">'
                    f'<span style="font-family: Consolas, monospace; font-weight: 600; color: {param_name_color};">'
                    f'• {html.escape(p_name)}</span>'
                )
                if p_desc:
                    html_parts.append(
                        f': <span style="color: {param_desc_color};">{html.escape(p_desc)}</span>'
                    )
                html_parts.append('</div>')

            if len(params) > max_params:
                remaining = len(params) - max_params
                html_parts.append(
                    f'<div style="font-size: 10px; color: {meta_color}; padding-left: 6px; font-style: italic;">'
                    f'... and {remaining} more parameters'
                    f'</div>'
                )
            html_parts.append('</div>')

        # Returns section
        if returns and kind not in ("constant",):
            html_parts.append(
                f'<div style="border-top: 1px solid {sep_color}; padding-top: 4px; margin-top: 4px; '
                f'font-size: 11px; color: {meta_color};">'
                f'<b>Returns:</b> {html.escape(returns)}'
                f'</div>'
            )

        # If there is another common variant
        if len(entries) > 1 and entries[1].get("parent") and entries[1].get("parent") != parent:
            alt_parent = entries[1].get("parent")
            html_parts.append(
                f'<div style="border-top: 1px solid {sep_color}; padding-top: 4px; margin-top: 4px; '
                f'font-size: 10px; color: {meta_color}; font-style: italic;">'
                f'Also defined in {html.escape(alt_parent)}'
                f'</div>'
            )

        html_parts.append('</div>')
        return "".join(html_parts)
