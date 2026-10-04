import os
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPixmap


def get_data_dir():
    if os.name == "nt":
        base = os.getenv("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~/.config")
    return os.path.join(base, "MP3Downloader")


def get_downloads_dir():
    return str(Path.home() / "Downloads")


def set_circular_pixmap(pixmap: QPixmap, size: int = 64) -> QPixmap:
    if pixmap.isNull():
        return QPixmap(size, size)

    scaled = pixmap.scaledToWidth(size, Qt.SmoothTransformation)
    circular = QPixmap(size, size)
    circular.fill(Qt.transparent)

    painter = QPainter(circular)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor("white"))
    painter.drawEllipse(0, 0, size, size)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.drawPixmap(0, 0, scaled)
    painter.end()
    return circular


def format_speed(speed: float) -> str:
    units = ["B/s", "KB/s", "MB/s", "GB/s"]
    value = speed
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{speed:.2f} TB/s"


def format_time(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}h {minutes}m"
