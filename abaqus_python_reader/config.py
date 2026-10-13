import os
import json
from pathlib import Path

DEFAULT_CONFIG = {
    "last_file": "abaqus.rpy",
    "topmost": True,
    "opacity": 92,               # 10 - 100
    "frameless": True,
    "auto_scroll": True,
    "word_wrap": True,
    "filter_viewport": True,     # True: filter out viewport rotate/pan/zoom
    "dark_theme": False,
    "show_line_numbers": True,
    "font_family": "Consolas",
    "font_size": 10,
    "window_x": 200,
    "window_y": 150,
    "window_width": 780,
    "window_height": 320,
    "language": "en",           # "en" or "zh"
    "hover_doc": True,          # True: show Abaqus API doc on hover
    "partition_blocks": True,   # True: partition code into distinct functional blocks
}

CONFIG_FILE = Path(__file__).resolve().parent / "config.json"

class ConfigManager:
    def __init__(self, filepath=CONFIG_FILE):
        self.filepath = filepath
        self.settings = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception as e:
                print(f"[Config] Error loading settings: {e}")

    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Config] Error saving settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
