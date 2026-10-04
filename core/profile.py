import json
import os

from core.utils import get_data_dir, get_downloads_dir


class UserProfile:
    def __init__(self):
        self.profile_file = os.path.join(get_data_dir(), "profile.json")
        self.data = self.load_profile()

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
        os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
        with open(self.profile_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def set_username(self, username: str):
        self.data["username"] = username or "PNG User"
        self.save_profile()

    def set_profile_picture(self, path: str):
        self.data["profile_picture"] = path
        self.save_profile()

    def get_username(self):
        return self.data.get("username", "PNG User")

    def get_download_path(self):
        return self.data.get("download_path", get_downloads_dir())

    def set_download_path(self, path: str):
        self.data["download_path"] = path
        self.save_profile()

    def get_audio_format(self):
        return self.data.get("audio_format", "mp3")

    def set_audio_format(self, fmt: str):
        self.data["audio_format"] = fmt
        self.save_profile()

    def get_audio_quality(self):
        return self.data.get("audio_quality", "192")

    def set_audio_quality(self, quality: str):
        self.data["audio_quality"] = quality
        self.save_profile()

    def get_theme(self):
        return self.data.get("theme", "dark")

    def set_theme(self, theme: str):
        self.data["theme"] = theme
        self.save_profile()

    def is_profile_complete(self):
        return bool(self.data.get("username", "").strip())
