import os
from pathlib import Path
from PySide6.QtCore import QObject, QTimer, Signal

from .i18n import tr


class FileMonitor(QObject):
    # Signals
    new_content_appended = Signal(str)
    file_reset = Signal()
    file_status_changed = Signal(bool, str) # is_active, message

    def __init__(self, check_interval_ms=250):
        super().__init__()
        self.filepath = ""
        self.last_pos = 0
        self.last_mtime = 0
        self.is_monitoring = False

        self.timer = QTimer(self)
        self.timer.setInterval(check_interval_ms)
        self.timer.timeout.connect(self._check_file)

    def refresh_status(self):
        """Re-evaluates file status and emits status signal with current language."""
        self._check_file(initial_load=False)

    def set_file(self, filepath: str):
        self.filepath = os.path.abspath(filepath) if filepath else ""
        self.last_pos = 0
        self.last_mtime = 0
        self.file_reset.emit()
        self._check_file(initial_load=True)

    def start(self):
        if not self.timer.isActive():
            self.timer.start()

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()

    def reload(self):
        self.last_pos = 0
        self.last_mtime = 0
        self.file_reset.emit()
        self._check_file(initial_load=True)

    def _check_file(self, initial_load=False):
        if not self.filepath:
            self.file_status_changed.emit(False, tr("status_no_file"))
            return

        if not os.path.isfile(self.filepath):
            self.file_status_changed.emit(
                False, tr("status_file_not_found", filename=os.path.basename(self.filepath))
            )
            return

        try:
            stat = os.stat(self.filepath)
            current_mtime = stat.st_mtime
            current_size = stat.st_size

            # Check if file was truncated/overwritten by a new Abaqus session
            if current_size < self.last_pos:
                self.last_pos = 0
                self.file_reset.emit()

            # If file size increased or mtime changed or first load
            if current_size > self.last_pos or initial_load or current_mtime != self.last_mtime:
                self._read_new_content(current_size)
                self.last_mtime = current_mtime
                self.file_status_changed.emit(
                    True, tr("status_monitoring", filename=os.path.basename(self.filepath))
                )

        except Exception as e:
            self.file_status_changed.emit(
                False, tr("status_read_error", error=str(e)[:30])
            )

    def _read_new_content(self, current_size):
        try:
            # Open with shared read (Windows default for Python 'r' mode allows writes)
            with open(self.filepath, "r", encoding="utf-8", errors="replace") as f:
                f.seek(self.last_pos)
                new_text = f.read()
                self.last_pos = f.tell()

            if new_text:
                self.new_content_appended.emit(new_text)
        except Exception as e:
            # Fallback for encoding (e.g. GBK/GB2312 or ANSI if Abaqus used local encoding)
            try:
                with open(self.filepath, "r", encoding="gbk", errors="replace") as f:
                    f.seek(self.last_pos)
                    new_text = f.read()
                    self.last_pos = f.tell()
                if new_text:
                    self.new_content_appended.emit(new_text)
            except Exception as e2:
                print(f"[FileMonitor] Read error: {e2}")
