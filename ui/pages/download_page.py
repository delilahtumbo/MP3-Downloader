import json
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.downloader import DownloadTask


class DownloadPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        title = QLabel("Download")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste a YouTube or supported media URL here")
        layout.addWidget(self.url_input)

        format_row = QHBoxLayout()
        format_label = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp3", "m4a", "wav", "aac", "flac", "opus", "vorbis"])
        self.format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        format_row.addWidget(format_label)
        format_row.addWidget(self.format_combo)
        layout.addLayout(format_row)

        quality_row = QHBoxLayout()
        quality_label = QLabel("Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["128", "192", "256", "320"])
        self.quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        quality_row.addWidget(quality_label)
        quality_row.addWidget(self.quality_combo)
        layout.addLayout(quality_row)

        add_btn = QPushButton("➕ Add to Queue")
        add_btn.clicked.connect(self.add_to_queue)
        layout.addWidget(add_btn)
        layout.addStretch()

    def add_to_queue(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a valid URL.")
            return

        task = DownloadTask(
            url=url,
            output_path=self.parent.user_profile.get_download_path(),
            audio_format=self.format_combo.currentText(),
            audio_quality=self.quality_combo.currentText(),
            playlist=False,
        )
        self.parent.download_queue.append(task)
        self.parent.queue_page.refresh_queue()
        self.url_input.clear()
        self.parent.show_info("Added", "Download task added to the queue.")


QueuePage = None
