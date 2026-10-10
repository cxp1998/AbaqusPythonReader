import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from abaqus_python_reader.app import MainWindow, get_vector_icon


def main():
    # Enable High DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("AbaqusPythonReader")
    app.setApplicationDisplayName("AbaqusPythonReader")

    app_icon = get_vector_icon()
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
