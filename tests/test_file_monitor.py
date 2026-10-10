import sys
import tempfile
import unittest
from pathlib import Path
from PySide6.QtCore import QCoreApplication
from python_reader.file_monitor import FileMonitor


class TestFileMonitor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QCoreApplication.instance()
        if cls.app is None:
            cls.app = QCoreApplication(sys.argv)

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "abaqus.rpy"
        self.test_file.write_text("line 1\nline 2\n", encoding="utf-8")
        self.received_chunks = []

    def tearDown(self):
        self.temp_dir.cleanup()

    def _on_chunk(self, text):
        self.received_chunks.append(text)

    def test_file_monitor_initial_read_and_append(self):
        monitor = FileMonitor(check_interval_ms=50)
        monitor.new_content_appended.connect(self._on_chunk)
        monitor.set_file(str(self.test_file))

        self.assertEqual(len(self.received_chunks), 1)
        self.assertIn("line 1", self.received_chunks[0])

        # Append new lines
        with open(self.test_file, "a", encoding="utf-8") as f:
            f.write("line 3\n")

        monitor._check_file()
        self.assertEqual(len(self.received_chunks), 2)
        self.assertEqual(self.received_chunks[1], "line 3\n")


if __name__ == "__main__":
    unittest.main()
