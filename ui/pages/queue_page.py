from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class QueuePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        title = QLabel("Download Queue")
        title.setFont(self.parent.font())
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels(["URL", "Format", "Quality", "Status", "Progress"])
        self.queue_table.setAlternatingRowColors(True)
        layout.addWidget(self.queue_table)

        button_row = QHBoxLayout()
        start_btn = QPushButton("▶ Start Queue")
        start_btn.clicked.connect(self.start_queue)
        button_row.addWidget(start_btn)

        remove_btn = QPushButton("❌ Remove Selected")
        remove_btn.clicked.connect(self.remove_selected)
        button_row.addWidget(remove_btn)

        clear_btn = QPushButton("🗑 Clear All")
        clear_btn.clicked.connect(self.clear_queue)
        button_row.addWidget(clear_btn)

        layout.addLayout(button_row)
        layout.addStretch()

        self.refresh_queue()

    def refresh_queue(self):
        tasks = self.parent.download_queue
        self.queue_table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            self.queue_table.setItem(row, 0, QTableWidgetItem(task.url))
            self.queue_table.setItem(row, 1, QTableWidgetItem(task.audio_format))
            self.queue_table.setItem(row, 2, QTableWidgetItem(f"{task.audio_quality} kbps"))
            self.queue_table.setItem(row, 3, QTableWidgetItem(task.status.upper()))
            self.queue_table.setItem(row, 4, QTableWidgetItem(f"{task.progress}%"))

    def start_queue(self):
        if not self.parent.download_queue:
            self.parent.show_warning("Empty Queue", "No downloads are queued.")
            return
        self.parent.show_info("Queue Started", f"Processing {len(self.parent.download_queue)} item(s).")

    def remove_selected(self):
        row = self.queue_table.currentRow()
        if row >= 0:
            self.parent.download_queue.pop(row)
            self.refresh_queue()

    def clear_queue(self):
        self.parent.download_queue.clear()
        self.refresh_queue()
