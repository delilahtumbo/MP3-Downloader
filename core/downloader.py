import os
import re
import shutil
import subprocess
from pathlib import Path

from PySide6.QtCore import QObject, Signal
import yt_dlp


def _is_valid_ffmpeg_binary(path):
    if not path or not os.path.isfile(path):
        return False
    try:
        result = subprocess.run(
            [path, "-hide_banner", "-f", "lavfi", "-i", "sine=frequency=1000:duration=0.1", "-c:a", "libmp3lame", "-f", "null", "-"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def resolve_ffmpeg_path():
    env_value = os.environ.get("FFMPEG_PATH")
    candidates = []

    if env_value:
        candidates.append(env_value)

    for path in os.environ.get("PATH", "").split(os.pathsep):
        if path:
            candidates.append(os.path.join(path, "ffmpeg.exe"))
            candidates.append(os.path.join(path, "ffmpeg"))

    candidates.extend([
        r"C:\Users\thelm\AppData\Local\Microsoft\WinGet\Packages\BtbN.FFmpeg.GPL.9.0_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-n9.0.1-11-ge47273f4d9-win64-gpl-9.0\bin\ffmpeg.exe",
        r"C:\Users\thelm\ffmpeg\ffmpeg.exe",
        r"C:\Users\thelm\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
    ])

    seen = set()
    for candidate in candidates:
        cleaned = str(candidate).strip().strip('"')
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        if _is_valid_ffmpeg_binary(cleaned):
            return cleaned

    seen.clear()
    for candidate in candidates:
        cleaned = str(candidate).strip().strip('"')
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        if os.path.isfile(cleaned):
            return cleaned

    return None


def ffmpeg_available():
    ffmpeg_path = resolve_ffmpeg_path()
    if ffmpeg_path:
        os.environ["FFMPEG_PATH"] = ffmpeg_path
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        current_path = os.environ.get("PATH", "")
        paths = current_path.split(os.pathsep) if current_path else []
        if ffmpeg_dir not in paths:
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + current_path if current_path else ffmpeg_dir
        return True
    return False


class DownloadTask:
    VALID_BITRATES = {"128k", "192k", "320k"}

    def __init__(self, url: str, output_path: str, audio_only: bool = True,
                 audio_format: str = "mp3", audio_quality: str = "192k",
                 playlist: bool = False):
        self.url = url
        self.output_path = str(output_path)
        self.audio_only = audio_only
        self.audio_format = str(audio_format or "mp3").lower()
        self.audio_quality = self.normalize_bitrate(audio_quality)
        self.playlist = playlist
        self.status = "pending"
        self.progress = 0
        self.error = None
        self._from_queue = False
        self.progress_callback = None
        self.converted_file = None

    @staticmethod
    def normalize_bitrate(value):
        normalized = str(value or "192k").strip().lower()
        if normalized.endswith("k") and normalized[:-1].isdigit():
            bitrate = normalized[:-1]
            if bitrate in {"128", "192", "320"}:
                return f"{bitrate}k"
        if normalized.isdigit() and normalized in {"128", "192", "320"}:
            return f"{normalized}k"
        return "192k"

    def get_bitrate_kbps(self):
        return int(self.audio_quality.replace("k", ""))

    def should_convert_to_mp3(self):
        return True

    def execute(self, progress_callback=None):
        try:
            if self.audio_only and not ffmpeg_available():
                self.status = "error"
                self.error = (
                    "FFmpeg was not found. Please install FFmpeg and make sure it is on your PATH."
                )
                return False

            self.progress_callback = progress_callback
            self.status = "downloading"
            Path(self.output_path).mkdir(parents=True, exist_ok=True)

            options = {
                "format": "bestaudio/best" if self.audio_only else "best",
                "outtmpl": os.path.join(self.output_path, "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
                "noplaylist": not self.playlist,
                "progress_hooks": [self._progress_hook] if progress_callback else [],
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([self.url])

            source_file = self._find_downloaded_audio(Path(self.output_path))
            if source_file is None:
                self.status = "error"
                self.error = "No audio file was downloaded."
                return False

            converted_file = self._convert_to_mp3(source_file, Path(self.output_path))
            if converted_file is None:
                self.status = "error"
                self.error = self.error or "MP3 conversion failed."
                return False

            self.converted_file = str(converted_file)

            if source_file.exists() and source_file != converted_file:
                try:
                    source_file.unlink()
                except OSError:
                    pass

            self.status = "completed"
            self.progress = 100
            if self.progress_callback:
                self.progress_callback(100)
            return True
        except Exception as exc:
            self.status = "error"
            self.error = str(exc)
            return False

    def _find_downloaded_audio(self, directory: Path):
        candidates = sorted(directory.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
        for item in candidates:
            if not item.is_file():
                continue
            if item.suffix.lower() == ".mp3":
                return item
            if item.suffix.lower() not in {".part", ".f248", ".f251", ".f302", ".tmp"}:
                return item
        return None

    def _convert_to_mp3(self, source_file: Path, output_dir: Path):
        if source_file.suffix.lower() == ".mp3":
            self.converted_file = str(source_file)
            return source_file

        converted_path = output_dir / f"{source_file.stem}.mp3"
        ffmpeg_path = resolve_ffmpeg_path() or shutil.which("ffmpeg") or os.environ.get("FFMPEG_PATH")
        if not ffmpeg_path:
            self.status = "error"
            self.error = "FFmpeg is not installed or not on PATH."
            return None

        os.environ["FFMPEG_PATH"] = ffmpeg_path

        command = [
            ffmpeg_path,
            "-i",
            str(source_file),
            "-vn",
            "-ar",
            "44100",
            "-acodec",
            "libmp3lame",
            "-b:a",
            self.audio_quality,
            "-y",
            str(converted_path),
        ]

        self.status = "converting"
        if self.progress_callback:
            self.progress_callback(90)

        stderr_buffer = []
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                errors="replace",
            )
            total_duration = None
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                if not line:
                    continue

                stderr_buffer.append(line.rstrip())

                duration_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", line)
                if duration_match:
                    total_seconds = (
                        int(duration_match.group(1)) * 3600
                        + int(duration_match.group(2)) * 60
                        + float(duration_match.group(3))
                    )
                    total_duration = total_seconds

                time_match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
                if time_match and total_duration and total_duration > 0:
                    current_seconds = (
                        int(time_match.group(1)) * 3600
                        + int(time_match.group(2)) * 60
                        + float(time_match.group(3))
                    )
                    progress = max(90, min(99, int((current_seconds / total_duration) * 100)))
                    self.progress = progress
                    if self.progress_callback:
                        self.progress_callback(progress)

            process.wait(timeout=120)
            if process.returncode != 0:
                err_text = "\n".join(stderr_buffer[-15:]).strip()
                self.error = err_text or f"FFmpeg exited with code {process.returncode}."
                return None
        except Exception as exc:
            self.error = str(exc)
            return None

        if converted_path.exists():
            self.converted_file = str(converted_path)
            self.progress = 100
            if self.progress_callback:
                self.progress_callback(100)
            return converted_path
        return None

    def _progress_hook(self, data):
        if data.get("status") == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            downloaded = data.get("downloaded_bytes") or 0
            if total > 0:
                self.progress = int((downloaded / total) * 80)
                if self.progress_callback:
                    self.progress_callback(self.progress)
        elif data.get("status") == "finished":
            self.progress = 85
            if self.progress_callback:
                self.progress_callback(85)


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
