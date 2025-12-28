"""
REST API for DiscordSoundsU
Provides endpoints to control sound playback
"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from .sounds_manager import SoundsManager
from .utils import play_audio

logger = logging.getLogger(__name__)


class SoundsAPI:
    def __init__(self, bot, sounds_manager: SoundsManager):
        self.bot = bot
        self.sounds_manager = sounds_manager
        self.app = FastAPI(title="DiscordSoundsU API")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.post("/play/{sound_name}")
        async def play_sound(sound_name: str):
            """
            Play a sound in the bot's current voice channel.

            Args:
                sound_name: Name of the sound to play (without .mp3 extension)

            Returns:
                JSON response with status
            """
            # Check if sound exists
            available_sounds = self.sounds_manager.update_sounds()
            if sound_name not in available_sounds:
                raise HTTPException(
                    status_code=404,
                    detail=f"Sound '{sound_name}' not found. Available sounds: {', '.join(available_sounds)}",
                )

            # Get bot's voice client
            voice_client = None
            for vc in self.bot.voice_clients:
                if vc.is_connected():
                    voice_client = vc
                    break

            if not voice_client or not voice_client.is_connected():
                raise HTTPException(
                    status_code=503, detail="Bot is not connected to any voice channel"
                )

            if voice_client and voice_client.is_playing():
                voice_client.stop()
                logger.info("Stopped currently playing sound")

            # Play the sound
            error = play_audio(sound_name, voice_client)

            if error:
                raise HTTPException(status_code=400, detail=error)

            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "message": f"Playing sound: {sound_name}",
                },
            )
        
        @self.app.post("/stop")
        async def stop_sound():
            """
            Stop any currently playing sound.
            """

            # Get bot's voice client
            voice_client = None
            for vc in self.bot.voice_clients:
                if vc.is_connected():
                    voice_client = vc
                    break

            if not voice_client or not voice_client.is_connected():
                raise HTTPException(
                    status_code=503, detail="Bot is not connected to any voice channel"
                )

            if voice_client and voice_client.is_playing():
                voice_client.stop()
                logger.info("Stopped currently playing sound")
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "message": "Stopped playing sound",
                    },
                )
            else:
                return JSONResponse(
                    status_code=200,
                    content={
                        "status": "success",
                        "message": "No sound was playing",
                    },
                )
                

        @self.app.get("/sounds")
        async def list_sounds():
            """
            List all available sounds.

            Returns:
                List of available sound names
            """
            sounds = self.sounds_manager.update_sounds()
            return JSONResponse(status_code=200, content={"sounds": sorted(sounds)})

        @self.app.get("/status")
        async def bot_status():
            """
            Get the bot's connection status.

            Returns:
                JSON with bot status and connected voice channel
            """
            voice_client = None
            for vc in self.bot.voice_clients:
                if vc.is_connected():
                    voice_client = vc
                    break

            if voice_client:
                return JSONResponse(
                    status_code=200,
                    content={
                        "connected": True,
                        "voice_channel": voice_client.channel.name,
                        "guild": voice_client.guild.name,
                    },
                )
            else:
                return JSONResponse(status_code=200, content={"connected": False})
