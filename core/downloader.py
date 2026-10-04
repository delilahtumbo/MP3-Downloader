import os
from pathlib import Path

import yt_dlp


class DownloadTask:
    def __init__(self, url: str, output_path: str, audio_only: bool = True,
                 audio_format: str = "mp3", audio_quality: str = "192"):
        self.url = url
        self.output_path = output_path
        self.audio_only = audio_only
        self.audio_format = audio_format
        self.audio_quality = audio_quality
        self.status = "pending"
        self.progress = 0
        self.error = None

    def execute(self, progress_callback=None):
        try:
            self.status = "downloading"
            Path(self.output_path).mkdir(parents=True, exist_ok=True)

            options = {
                "format": "bestaudio/best" if self.audio_only else "best",
                "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
                "quiet": False,
                "no_warnings": False,
                "noplaylist": False,
                "progress_hooks": [self._progress_hook] if progress_callback else [],
            }

            if self.audio_only:
                options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.audio_format,
                    "preferredquality": self.audio_quality,
                }]

            self.progress_callback = progress_callback

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])

            self.status = "completed"
            self.progress = 100
            return True
        except Exception as exc:
            self.status = "error"
            self.error = str(exc)
            return False

    def _progress_hook(self, data):
        if data.get("status") == "downloading":
            total = data.get("total_bytes", 0)
            downloaded = data.get("downloaded_bytes", 0)
            if total > 0:
                self.progress = int((downloaded / total) * 100)
                if self.progress_callback:
                    self.progress_callback(self.progress)


class DownloadQueue:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def clear_queue(self):
        self.tasks.clear()

    def get_queue(self):
        return self.tasks
