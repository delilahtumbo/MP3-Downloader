import json
import os
import shutil
from functools import lru_cache
from pathlib import Path

from PySide6.QtCore import QObject, Signal
import yt_dlp

from core.utils import get_data_dir, get_downloads_dir


@lru_cache(maxsize=1)
def ffmpeg_available():
    return shutil.which("ffmpeg") is not None or bool(os.environ.get("FFMPEG_PATH"))


class UserProfile:
    def __init__(self):
        self.profile_file = os.path.join(get_data_dir(), "profile.json")
        self.data = self.load_profile()
        self._dirty = False

    def load_profile(self):
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self.get_default_profile()

    def get_default_profile(self):
        return {
            "username": "PNG User",
            "profile_picture": "",
            "download_path": get_downloads_dir(),
            "audio_format": "mp3",
            "audio_quality": "192",
            "theme": "dark",
            "auto_update": True,
            "notifications": True,
        }

    def save_profile(self):
        if not self._dirty:
            return
        os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
        with open(self.profile_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)
        self._dirty = False

    def _set_value(self, key: str, value):
        self.data[key] = value
        self._dirty = True
        self.save_profile()

    def set_username(self, username: str):
        self._set_value("username", username or "PNG User")

    def set_profile_picture(self, path: str):
        self._set_value("profile_picture", path)

    def get_username(self):
        return self.data.get("username", "PNG User")

    def get_download_path(self):
        return self.data.get("download_path", get_downloads_dir())

    def set_download_path(self, path: str):
        self._set_value("download_path", path)

    def get_audio_format(self):
        return self.data.get("audio_format", "mp3")

    def set_audio_format(self, fmt: str):
        self._set_value("audio_format", fmt)

    def get_audio_quality(self):
        return self.data.get("audio_quality", "192")

    def set_audio_quality(self, quality: str):
        self._set_value("audio_quality", quality)

    def get_theme(self):
        return self.data.get("theme", "dark")

    def set_theme(self, theme: str):
        self._set_value("theme", theme)

    def is_profile_complete(self):
        return bool(self.data.get("username", "").strip())

    def update_profile(self, updates: dict):
        self.data.update(updates)
        self._dirty = True
        self.save_profile()


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
