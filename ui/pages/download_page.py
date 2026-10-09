import json
import os

from PySide6.QtCore import QPoint, QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
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
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(18)

        hero = QFrame()
        hero.setObjectName("heroCard")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 24, 24, 24)
        hero_layout.setSpacing(16)

        title = QLabel("Download MP3 from YouTube")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        hero_layout.addWidget(title)

        subtitle = QLabel("Paste a video link, choose your settings, and build your playlist in seconds.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #5b6472; font-size: 12px;")
        hero_layout.addWidget(subtitle)

        input_row = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=...")
        self.url_input.setMinimumHeight(52)
        input_row.addWidget(self.url_input, 1)

        add_btn = QPushButton("Add to Queue")
        add_btn.setMinimumHeight(52)
        add_btn.clicked.connect(self.add_to_queue)
        input_row.addWidget(add_btn)

        convert_btn = QPushButton("Download & Convert MP3")
        convert_btn.setMinimumHeight(52)
        convert_btn.clicked.connect(self.add_to_queue)
        input_row.addWidget(convert_btn)
        hero_layout.addLayout(input_row)

        options_row = QHBoxLayout()
        format_label = QLabel("Format")
        format_label.setStyleSheet("font-weight: 700; min-width: 70px;")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp3", "m4a", "wav", "aac", "flac", "opus", "vorbis"])
        self.format_combo.setCurrentText(self.parent.user_profile.get_audio_format())
        self.format_combo.setMinimumHeight(40)

        quality_label = QLabel("Quality")
        quality_label.setStyleSheet("font-weight: 700; min-width: 70px;")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["128k", "192k", "320k"])
        self.quality_combo.setCurrentText(self.parent.user_profile.get_audio_quality())
        self.quality_combo.setMinimumHeight(40)

        options_row.addWidget(format_label)
        options_row.addWidget(self.format_combo, 1)
        options_row.addWidget(quality_label)
        options_row.addWidget(self.quality_combo, 1)
        hero_layout.addLayout(options_row)

        stats_row = QHBoxLayout()
        for label, value in [("Fast", "4K speed"), ("Secure", "Private"), ("Quality", "320 kbps")]:
            pill = QFrame()
            pill.setObjectName("featureCard")
            pill_layout = QVBoxLayout(pill)
            pill_layout.setContentsMargins(12, 10, 12, 10)
            value_label = QLabel(value)
            value_label.setStyleSheet("font-size: 11px; color: #CE1126; font-weight: 700;")
            name_label = QLabel(label)
            name_label.setStyleSheet("font-size: 10px; color: #5b6472; text-transform: uppercase; letter-spacing: 1.2px;")
            pill_layout.addWidget(value_label)
            pill_layout.addWidget(name_label)
            self._animate_card(pill)
            stats_row.addWidget(pill)
        hero_layout.addLayout(stats_row)

        layout.addWidget(hero)

        feature_grid = QGridLayout()
        feature_grid.setSpacing(14)
        feature_cards = [
            ("Lightning fast", "Optimized download engine for quick MP3 conversion.", "#ff6b57"),
            ("Safe & private", "Your downloads stay local and under your control.", "#f7d66b"),
            ("Audio quality", "Choose from crisp 128 to premium 320 kbps audio.", "#3ddc97"),
        ]
        for index, (title, summary, accent) in enumerate(feature_cards):
            card = QFrame()
            card.setObjectName("featureCard")
            card.setMinimumHeight(120)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(18, 18, 18, 18)
            card_layout.setSpacing(8)

            dot = QLabel("●")
            dot.setStyleSheet(f"color: {accent}; font-size: 16px;")
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 14, QFont.Bold))
            summary_label = QLabel(summary)
            summary_label.setWordWrap(True)
            summary_label.setStyleSheet("color: #475569; font-size: 11px;")

            card_layout.addWidget(dot)
            card_layout.addWidget(title_label)
            card_layout.addWidget(summary_label)

            self._animate_card(card)
            feature_grid.addWidget(card, index // 3, index % 3)

        layout.addLayout(feature_grid)
        layout.addStretch()

    def _animate_card(self, widget):
        effect = QGraphicsDropShadowEffect(widget)
        effect.setBlurRadius(28)
        effect.setOffset(0, 10)
        effect.setColor(Qt.darkGray)
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(500)
        animation.setStartValue(QPoint(widget.x() - 18, widget.y()))
        animation.setEndValue(QPoint(widget.x(), widget.y()))
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()

    def add_to_queue(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a valid URL.")
            return

        self.parent.user_profile.set_audio_format("mp3")
        self.parent.user_profile.set_audio_quality(self.quality_combo.currentText())

        task = DownloadTask(
            url=url,
            output_path=self.parent.user_profile.get_download_path(),
            audio_format="mp3",
            audio_quality=self.quality_combo.currentText(),
            playlist=False,
        )
        self.parent.download_queue.append(task)
        self.parent.queue_page.refresh_queue()
        self.url_input.clear()
        self.parent.show_info("Added", "Download task added to the queue and will convert to MP3 automatically.")


QueuePage = None
