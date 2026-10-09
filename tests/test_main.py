import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from core.downloader import DownloadTask, resolve_ffmpeg_path
from core.profile import UserProfile
from ui.main_window import MainWindow


MODULE_PATH = "main.py"


def _load_main_module():
    spec = importlib.util.spec_from_file_location("main_module", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["main_module"] = module
    spec.loader.exec_module(module)
    return module


class MainStartupTest(unittest.TestCase):
    def test_main_imports_window_class_and_creates_it(self):
        module = _load_main_module()

        self.assertTrue(hasattr(module, "MainWindow"))

        class FakeWindow:
            def __init__(self):
                self.shown = False

            def show(self):
                self.shown = True

        class FakeApp:
            def setApplicationName(self, *_args, **_kwargs):
                pass

            def setApplicationVersion(self, *_args, **_kwargs):
                pass

            def exec(self):
                return 0

        fake_app = FakeApp()
        fake_window = FakeWindow()

        module.MainWindow = lambda: fake_window
        module.QApplication = lambda *_args, **_kwargs: fake_app
        module.sys = SimpleNamespace(argv=["prog"], exit=lambda code: None)

        module.main()

        self.assertTrue(fake_window.shown)

    def test_user_profile_forces_dark_theme(self):
        profile = UserProfile()
        profile.set_theme("light")
        self.assertEqual(profile.get_theme(), "dark")

    def test_download_task_converts_with_bitrate_kbps(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            fake_input = temp_path / "demo.webm"
            fake_input.write_bytes(b"fake-audio")

            task = DownloadTask(
                url="https://example.com/video",
                output_path=str(temp_path),
                audio_format="mp3",
                audio_quality="320k",
            )

            self.assertEqual(task.audio_quality, "320k")
            self.assertEqual(task.get_bitrate_kbps(), 320)
            self.assertTrue(task.should_convert_to_mp3())

    def test_resolve_ffmpeg_path_falls_back_to_common_windows_location(self):
        with patch("core.downloader.os.path.isfile", side_effect=lambda path: path == r"C:\Users\thelm\ffmpeg\ffmpeg.exe"), \
             patch.dict(os.environ, {"PATH": "", "FFMPEG_PATH": ""}, clear=True):
            self.assertEqual(resolve_ffmpeg_path(), r"C:\Users\thelm\ffmpeg\ffmpeg.exe")

    def test_history_records_downloaded_mp3(self):
        app = QApplication.instance() or QApplication([])
        window = MainWindow()
        with tempfile.TemporaryDirectory() as temp_dir:
            mp3_path = Path(temp_dir) / "demo.mp3"
            mp3_path.write_bytes(b"fake mp3")
            task = DownloadTask(url="https://example.com/video", output_path=temp_dir, audio_format="mp3", audio_quality="192k")
            task.converted_file = str(mp3_path)
            task.status = "completed"

            window.record_download_history(task)

            self.assertTrue(any(item.get("file") == str(mp3_path) for item in window.download_history))
            app.quit()

    def test_queue_download_now_button_and_tab_progress_panel_exist(self):
        app = QApplication.instance() or QApplication([])
        window = MainWindow()
        self.assertTrue(hasattr(window, "tab_progress_bar"))
        self.assertTrue(hasattr(window, "tab_progress_label"))
        self.assertEqual(window.queue_page.start_button.text(), "Download Now")
        app.quit()


if __name__ == "__main__":
    unittest.main()
