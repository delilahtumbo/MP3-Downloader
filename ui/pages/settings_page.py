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
    QFileDialog,
)


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        title = QLabel("Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        profile_group = QGroupBox("Profile")
        form_layout = QFormLayout(profile_group)
        self.username_input = QLineEdit()
        self.username_input.setText(self.parent.user_profile.get_username())
        form_layout.addRow("Username:", self.username_input)
        layout.addWidget(profile_group)

        download_group = QGroupBox("Download Preferences")
        download_layout = QFormLayout(download_group)

        self.download_path = QLineEdit()
        self.download_path.setText(self.parent.user_profile.get_download_path())
        self.download_path.setReadOnly(True)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.choose_download_path)

        path_row = QHBoxLayout()
        path_row.addWidget(self.download_path)
        path_row.addWidget(browse_btn)
        download_layout.addRow("Download folder:", path_row)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp3", "m4a", "wav", "aac", "flac", "opus", "vorbis"])
        self.format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        download_layout.addRow("Default format:", self.format_combo)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["128", "192", "256", "320"])
        self.quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        download_layout.addRow("Default quality:", self.quality_combo)

        layout.addWidget(download_group)

        app_group = QGroupBox("Application")
        app_layout = QVBoxLayout(app_group)
        self.auto_update = QCheckBox("Check for updates automatically")
        self.auto_update.setChecked(self.parent.user_profile.data.get("auto_update", True))
        self.notifications = QCheckBox("Enable notifications")
        self.notifications.setChecked(self.parent.user_profile.data.get("notifications", True))
        app_layout.addWidget(self.auto_update)
        app_layout.addWidget(self.notifications)
        layout.addWidget(app_group)

        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        layout.addStretch()

    def choose_download_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select download folder", self.parent.user_profile.get_download_path())
        if folder:
            self.download_path.setText(folder)

    def save_settings(self):
        self.parent.user_profile.set_username(self.username_input.text())
        self.parent.user_profile.set_download_path(self.download_path.text())
        self.parent.user_profile.set_audio_format(self.format_combo.currentText())
        self.parent.user_profile.set_audio_quality(self.quality_combo.currentText())
        self.parent.user_profile.data["auto_update"] = self.auto_update.isChecked()
        self.parent.user_profile.data["notifications"] = self.notifications.isChecked()
        self.parent.user_profile.save_profile()
        self.parent.username_label.setText(self.parent.user_profile.get_username())
        self.parent.show_info("Saved", "Your settings have been saved successfully.")
