from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class HistoryPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("pageContainer")
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget#pageContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(206,17,38,0.12),
                                            stop:0.4 rgba(23,27,34,0.92),
                                            stop:1 rgba(15,17,21,0.96));
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 18px;
            }
            QLabel { color: #f4f4f4; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(18)

        title = QLabel("Download History")
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #ffffff; letter-spacing: 0.4px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Title", "File", "URL", "Quality", "Time"])
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_table.setWordWrap(True)
        layout.addWidget(self.history_table)

        button_row = QHBoxLayout()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_history)
        button_row.addWidget(refresh_btn)
        button_row.addStretch()
        layout.addLayout(button_row)
        layout.addStretch()

        self.refresh_history()

    def refresh_history(self):
        entries = getattr(self.parent, "download_history", [])
        self.history_table.setRowCount(len(entries))

        for row, entry in enumerate(entries):
            title = entry.get("title", "")
            file_path = entry.get("file", "")
            url = entry.get("url", "")
            quality = entry.get("quality", "")
            time_value = entry.get("time", "")

            self.history_table.setItem(row, 0, QTableWidgetItem(title))
            self.history_table.setItem(row, 1, QTableWidgetItem(file_path))
            self.history_table.setItem(row, 2, QTableWidgetItem(url))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(quality)))
            self.history_table.setItem(row, 4, QTableWidgetItem(time_value))

        self.history_table.resizeColumnsToContents()
