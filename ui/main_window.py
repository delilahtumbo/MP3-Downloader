import json
import os

from core.utils import get_data_dir, get_downloads_dir


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

