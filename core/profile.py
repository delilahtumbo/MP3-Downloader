import os
import shutil
from functools import lru_cache
from pathlib import Path

from PySide6.QtCore import QObject, Signal
import yt_dlp


@lru_cache(maxsize=1)
def ffmpeg_available():
    return shutil.which("ffmpeg") is not None or bool(os.environ.get("FFMPEG_PATH"))


class DownloadTask:
    def __init__(self, url: str, output_path: str, audio_only: bool = True,
                 audio_format: str = "mp3", audio_quality: str = "192",
                 playlist: bool = False):
        self.url = url
        self.output_path = str(output_path)
        self.audio_only = audio_only
        self.audio_format = audio_format
        self.audio_quality = str(audio_quality)
        self.playlist = playlist
        self.status = "pending"
        self.progress = 0
        self.error = None
        self._from_queue = False
        self.progress_callback = None

    def execute(self, progress_callback=None):
        try:
            self.progress_callback = progress_callback

            if self.audio_only and not ffmpeg_available():
                self.status = "error"
                self.error = (
                    "FFmpeg was not found. Please install FFmpeg and make sure it is on your PATH."
                )
                return False

            self.status = "downloading"
            Path(self.output_path).mkdir(parents=True, exist_ok=True)

            options = {
                "format": "bestaudio/best" if self.audio_only else "best",
                "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
                "noplaylist": not self.playlist,
                "progress_hooks": [self._progress_hook] if progress_callback else [],
                "retries": 3,
                "fragment_retries": 3,
                "socket_timeout": 30,
            }

            if self.audio_only:
                options["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": self.audio_format,
                    "preferredquality": self.audio_quality,
                }]

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])

            self.status = "completed"
            self.progress = 100
            if self.progress_callback:
                self.progress_callback(100)
            return True
        except Exception as exc:
            self.status = "error"
            self.error = str(exc)
            if self.progress_callback:
                self.progress_callback(0)
            return False

    def _progress_hook(self, data):
        if data.get("status") == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            downloaded = data.get("downloaded_bytes") or 0
            if total > 0:
                self.progress = int((downloaded / total) * 100)
                if self.progress_callback:
                    self.progress_callback(self.progress)
        elif data.get("status") == "finished":
            self.progress = 100
            if self.progress_callback:
                self.progress_callback(100)


class DownloadWorker(QObject):
    progress = Signal(int)
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, task):
        super().__init__()
        self.task = task

    def run(self):
        try:
            success = self.task.execute(progress_callback=self._on_progress)
            if success:
                self.finished.emit(self.task)
            else:
                self.error.emit(self.task.error or "Download failed.")
        except Exception as exc:
            self.error.emit(str(exc))

    def _on_progress(self, value):
        self.progress.emit(value)

