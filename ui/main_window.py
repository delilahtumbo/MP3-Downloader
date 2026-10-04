import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from core.profile import UserProfile
from core.utils import set_circular_pixmap
from ui.pages.download_page import DownloadPage
from ui.pages.queue_page import QueuePage
from ui.pages.settings_page import SettingsPage
from ui.theme import DARK_STYLESHEET, LIGHT_STYLESHEET, PNG_COLORS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3 Downloader")
        self.resize(1200, 800)
        self.setMinimumSize(900, 650)

        self.user_profile = UserProfile()
        self.download_queue = []
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setStyleSheet(f"background-color: {PNG_COLORS['dark_panel']}; border-bottom: 2px solid {PNG_COLORS['primary_red']};")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(18, 12, 18, 12)

        profile_container = QHBoxLayout()
        self.profile_picture = QLabel()
        self.profile_picture.setFixedSize(48, 48)
        self.profile_picture.setStyleSheet("border-radius: 24px;")
        self.update_profile_picture()
        profile_container.addWidget(self.profile_picture)

        self.username_label = QLabel(self.user_profile.get_username())
        self.username_label.setFont(QFont("Arial", 12, QFont.Bold))
        profile_container.addWidget(self.username_label)

        top_layout.addLayout(profile_container)
        top_layout.addStretch()

        self.theme_button = QPushButton("🌙 Dark")
        self.theme_button.setFixedWidth(120)
        self.theme_button.clicked.connect(self.toggle_theme)
        top_layout.addWidget(self.theme_button)

        layout.addWidget(top_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.download_page = DownloadPage(self)
        self.queue_page = QueuePage(self)
        self.settings_page = SettingsPage(self)

        self.tabs.addTab(self.download_page, "Download")
        self.tabs.addTab(self.queue_page, "Queue")
        self.tabs.addTab(self.settings_page, "Settings")

        layout.addWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(300)
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)

    def update_profile_picture(self):
        pic_path = self.user_profile.data.get("profile_picture", "")
        if pic_path and os.path.exists(pic_path):
            pixmap = QPixmap(pic_path)
        else:
            pixmap = QPixmap(48, 48)
            pixmap.fill(Qt.gray)
        circular = set_circular_pixmap(pixmap, 48)
        self.profile_picture.setPixmap(circular)

    def apply_theme(self):
        theme = self.user_profile.get_theme()
        if theme == "dark":
            self.setStyleSheet(DARK_STYLESHEET)
            self.theme_button.setText("🌙 Dark")
        else:
            self.setStyleSheet(LIGHT_STYLESHEET)
            self.theme_button.setText("☀️ Light")

    def toggle_theme(self):
        theme = self.user_profile.get_theme()
        new_theme = "light" if theme == "dark" else "dark"
        self.user_profile.set_theme(new_theme)
        self.apply_theme()

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)
