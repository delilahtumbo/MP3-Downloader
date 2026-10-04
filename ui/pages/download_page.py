from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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

        title = QLabel("Download Audio")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_group = QGroupBox("Create Download")
        form_layout = QFormLayout(form_group)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste a video or audio URL here")
        self.url_input.setMinimumHeight(42)
        form_layout.addRow("URL:", self.url_input)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp3", "m4a", "wav", "aac", "flac", "opus", "vorbis"])
        self.format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        form_layout.addRow("Format:", self.format_combo)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["128", "192", "256", "320"])
        self.quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        form_layout.addRow("Quality (kbps):", self.quality_combo)

        self.playlist_checkbox = QCheckBox("Download Playlist")
        form_layout.addRow(self.playlist_checkbox)

        layout.addWidget(form_group)

        button_row = QHBoxLayout()
        download_btn = QPushButton("📥 Download")
        download_btn.clicked.connect(self.start_download)
        button_row.addWidget(download_btn)

        queue_btn = QPushButton("🧺 Add to Queue")
        queue_btn.clicked.connect(self.add_to_queue)
        button_row.addWidget(queue_btn)

        clear_btn = QPushButton("🗑 Reset")
        clear_btn.clicked.connect(self.clear_form)
        button_row.addWidget(clear_btn)

        layout.addLayout(button_row)
        layout.addStretch()

    def get_task(self):
        url = self.url_input.text().strip()
        if not url:
            self.parent.show_warning("Missing URL", "Please enter a valid URL.")
            return None

        return DownloadTask(
            url=url,
            output_path=self.parent.user_profile.get_download_path(),
            audio_only=True,
            audio_format=self.format_combo.currentText(),
            audio_quality=self.quality_combo.currentText(),
        )

    def start_download(self):
        task = self.get_task()
        if not task:
            return

        success = task.execute()
        if success:
            self.parent.show_info("Download Complete", f"Your file was downloaded successfully to:\n{task.output_path}")
        else:
            self.parent.show_warning("Download Failed", task.error or "Unknown download error.")

    def add_to_queue(self):
        task = self.get_task()
        if not task:
            return
        self.parent.download_queue.append(task)
        self.parent.queue_page.refresh_queue()
        self.parent.show_info("Added to Queue", "Your item was added to the download queue.")
        self.clear_form()

    def clear_form(self):
        self.url_input.clear()
        self.format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        self.quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        self.playlist_checkbox.setChecked(False)
