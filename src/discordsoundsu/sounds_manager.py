import os
from .utils import MP3_PATH
from discord import app_commands
from mutagen.mp3 import MP3, HeaderNotFoundError
import logging

logger = logging.getLogger(__name__)


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

    def get_sound_duration(self, sound: str):
        if sound not in self._sounds:
            logger.info(f"Sound {sound} does not exist")
            return 0
        
        try:
            audio = MP3(str(MP3_PATH / f"{sound}.mp3"))
            return audio.info.length
        except HeaderNotFoundError as error:
            logger.error(f"Error getting duration for sound {sound}: {error}")
            return 0
        
