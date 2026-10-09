import json
import os

from PySide6.QtCore import Qt, QThread
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

from core.downloader import DownloadWorker
from core.profile import UserProfile
from core.utils import set_circular_pixmap
from ui.pages.download_page import DownloadPage
from ui.pages.history_page import HistoryPage
from ui.pages.queue_page import QueuePage
from ui.pages.settings_page import SettingsPage
from ui.theme import DARK_STYLESHEET, PNG_COLORS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MP3 Downloader")
        self.resize(1200, 800)
        self.setMinimumSize(900, 650)

        self.user_profile = UserProfile()
        self.download_queue = []
        self.download_history = []
        self.active_task = None
        self.worker = None
        self.worker_thread = None
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top_bar = QWidget()
        self.top_bar.setObjectName("topBar")
        self.top_bar.setStyleSheet(f"background-color: {PNG_COLORS['dark_panel']}; border-bottom: 2px solid {PNG_COLORS['primary_red']};")
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(18, 12, 18, 12)

        brand_container = QHBoxLayout()
        self.profile_picture = QLabel()
        self.profile_picture.setFixedSize(40, 40)
        self.profile_picture.setStyleSheet("border-radius: 20px;")
        self.update_profile_picture()
        brand_container.addWidget(self.profile_picture)

        self.username_label = QLabel(self.user_profile.get_username())
        self.username_label.setFont(QFont("Arial", 11, QFont.Bold))
        brand_container.addWidget(self.username_label)

        self.app_name_label = QLabel("MP3 Downloader")
        self.app_name_label.setStyleSheet("font-size: 15px; font-weight: 700; letter-spacing: 0.5px;")
        self.app_name_label.setContentsMargins(18, 0, 0, 0)
        brand_container.addWidget(self.app_name_label)

        top_layout.addLayout(brand_container)
        top_layout.addStretch()

        self.theme_button = QPushButton("Dark Mode")
        self.theme_button.setFixedWidth(120)
        self.theme_button.setEnabled(False)
        self.theme_button.setStyleSheet("background: rgba(255,255,255,0.05); color: #f4f4f4; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;")
        top_layout.addWidget(self.theme_button)

        layout.addWidget(self.top_bar)

        self.nav_bar = QWidget()
        self.nav_bar.setObjectName("navBar")
        self.nav_bar.setStyleSheet("background-color: rgba(23, 27, 34, 0.9); border-bottom: 1px solid rgba(255,255,255,0.06);")
        nav_layout = QHBoxLayout(self.nav_bar)
        nav_layout.setContentsMargins(18, 10, 18, 10)
        nav_layout.setSpacing(10)
        self.nav_buttons = []
        for idx, label in enumerate(["Home", "Queue", "History", "Settings"]):
            button = QPushButton(label)
            button.setMinimumHeight(36)
            button.setProperty("nav", True)
            button.clicked.connect(lambda _checked=False, i=idx: self.tabs.setCurrentIndex(i))
            if idx == 0:
                button.setStyleSheet("background: #CE1126; color: white; border-radius: 10px;")
            else:
                button.setStyleSheet("background: rgba(255,255,255,0.04); color: #e8e8e8; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;")
            self.nav_buttons.append(button)
            nav_layout.addWidget(button)
        nav_layout.addStretch()
        layout.addWidget(self.nav_bar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.download_page = DownloadPage(self)
        self.queue_page = QueuePage(self)
        self.history_page = HistoryPage(self)
        self.settings_page = SettingsPage(self)

        self.tabs.addTab(self.download_page, "Download")
        self.tabs.addTab(self.queue_page, "Queue")
        self.tabs.addTab(self.history_page, "History")
        self.tabs.addTab(self.settings_page, "Settings")
        self.tabs.currentChanged.connect(self._update_nav_style)

        layout.addWidget(self.tabs)

        self.tab_progress_panel = QWidget()
        self.tab_progress_panel.setObjectName("tabProgressPanel")
        tab_progress_layout = QVBoxLayout(self.tab_progress_panel)
        tab_progress_layout.setContentsMargins(18, 10, 18, 10)
        tab_progress_layout.setSpacing(6)

        self.tab_progress_label = QLabel("No active download")
        self.tab_progress_label.setStyleSheet("font-size: 11px; color: #d7d7d7;")
        tab_progress_layout.addWidget(self.tab_progress_label)

        self.tab_progress_bar = QProgressBar()
        self.tab_progress_bar.setRange(0, 100)
        self.tab_progress_bar.setValue(0)
        self.tab_progress_bar.setVisible(False)
        tab_progress_layout.addWidget(self.tab_progress_bar)

        layout.addWidget(self.tab_progress_panel)

        self.status_bar = QStatusBar()
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(300)
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.status_bar.showMessage("Ready")
        self.setStatusBar(self.status_bar)
        self._hide_tab_progress()

    def _update_nav_style(self, index):
        active = "background: #CE1126; color: white; border-radius: 10px;"
        inactive = "background: rgba(255,255,255,0.04); color: #e8e8e8; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;"

        for i, button in enumerate(self.nav_buttons):
            button.setStyleSheet(active if i == index else inactive)

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
        self.setStyleSheet(DARK_STYLESHEET)
        self.top_bar.setStyleSheet(f"background-color: {PNG_COLORS['dark_panel']}; border-bottom: 2px solid {PNG_COLORS['primary_red']};")
        self.nav_bar.setStyleSheet("background-color: rgba(23, 27, 34, 0.9); border-bottom: 1px solid rgba(255,255,255,0.06);")
        self.theme_button.setText("Dark Mode")
        self._update_nav_style(self.tabs.currentIndex())

    def toggle_theme(self):
        self.user_profile.set_theme("dark")
        self.apply_theme()

    def show_warning(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def start_download_task(self, task, from_queue=False):
        if task is None:
            return

        self.active_task = task
        task._from_queue = from_queue
        self.status_bar.showMessage(f"Downloading {task.url[:60]}{'...' if len(task.url) > 60 else ''}")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self._show_tab_progress(f"Downloading MP3: {task.url[:45]}{'...' if len(task.url) > 45 else ''}", 0, True)

        self.worker_thread = QThread(self)
        self.worker = DownloadWorker(task)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._on_download_progress)
        self.worker.finished.connect(self._on_download_finished)
        self.worker.error.connect(self._on_download_error)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.error.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()

    def _show_tab_progress(self, text, value=0, visible=True):
        self.tab_progress_label.setText(text)
        self.tab_progress_bar.setValue(value)
        self.tab_progress_bar.setVisible(visible)

    def _hide_tab_progress(self):
        self.tab_progress_label.setText("No active download")
        self.tab_progress_bar.setValue(0)
        self.tab_progress_bar.setVisible(False)

    def _on_download_progress(self, value):
        self.progress_bar.setValue(value)
        self.status_bar.showMessage(f"Downloading... {value}%")
        self._show_tab_progress(f"MP3 download in progress: {value}%", value, True)
        if self.queue_page is not None:
            self.queue_page.refresh_queue()

    def _on_download_finished(self, task):
        self.record_download_history(task)
        self.active_task = None
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Download complete: {task.url}")
        self._show_tab_progress(f"Download complete: {os.path.basename(task.converted_file or task.url)}", 100, True)
        if self.queue_page is not None:
            self.queue_page.refresh_queue()
        if self.history_page is not None:
            self.history_page.refresh_history()

        if self.download_queue:
            self.process_queue()
        else:
            self._hide_tab_progress()

    def _on_download_error(self, message):
        self.active_task = None
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Download failed")
        self._show_tab_progress("Download failed", 0, True)
        if self.queue_page is not None:
            self.queue_page.refresh_queue()
        self.show_warning("Download Error", message)

        if self.download_queue:
            self.process_queue()
        else:
            self._hide_tab_progress()

    def process_queue(self):
        if self.active_task is not None or not self.download_queue:
            return

        task = self.download_queue.pop(0)
        self.start_download_task(task, from_queue=True)
        if self.queue_page is not None:
            self.queue_page.refresh_queue()

    def record_download_history(self, task):
        file_path = getattr(task, "converted_file", None) or getattr(task, "output_path", None)
        if not file_path or not str(file_path).lower().endswith(".mp3"):
            return

        item = {
            "title": os.path.basename(file_path),
            "file": os.path.abspath(file_path),
            "url": task.url,
            "quality": task.audio_quality,
            "time": __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.download_history.insert(0, item)
        if self.history_page is not None:
            self.history_page.refresh_history()


__all__ = ["MainWindow", "UserProfile"]
