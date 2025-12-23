import os
from .utils import MP3_PATH
from discord import app_commands


class SoundsManager:
    def __init__(self):
        self._sounds = [
            os.path.splitext(f)[0] for f in os.listdir(MP3_PATH) if f.endswith(".mp3")
        ]

    def update_sounds(self):
        self._sounds = [
            os.path.splitext(f)[0] for f in os.listdir(MP3_PATH) if f.endswith(".mp3")
        ]
        return self._sounds

    def sound_autocomplete(self, current: str, limit: int = 25):
        return [
            app_commands.Choice(name=option, value=option)
            for option in self._sounds
            if current.lower() in option.lower()
        ][:limit]
