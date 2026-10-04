#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from core.utils import get_data_dir
from ui.main_window import MainWindow


def main():
    data_dir = get_data_dir()
    Path(data_dir).mkdir(parents=True, exist_ok=True)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    app.setApplicationName("MP3 Downloader")
    app.setApplicationVersion("1.0.0")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
