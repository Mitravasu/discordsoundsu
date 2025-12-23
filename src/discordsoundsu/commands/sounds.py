"""
Commands related to sounds operations.

- List sounds
- Play sound
- Upload sound
- Delete sound
"""

import logging
import os

from typing import List
from discord.ext.commands import Bot, Cog
from discord import Interaction, app_commands, VoiceClient, Attachment

from ..utils import MP3_PATH, play_audio
from ..sounds_manager import SoundsManager

logger = logging.getLogger(__name__)


class SoundCommands(Cog):
    def __init__(self, bot: Bot, sounds_manager: SoundsManager):
        self.bot = bot
        self.sounds_manager = sounds_manager

    @app_commands.command(name="ls", description="Lists available sounds")
    async def ls(self, interaction: Interaction):
        sounds = self.sounds_manager.update_sounds()
        if not sounds:
            return await interaction.response.send_message("No sounds available.")

        sound_list = "\n".join(sounds)
        await interaction.response.send_message(
            f"Available sounds:\n```\n{sound_list}\n```"
        )

    @app_commands.command(name="play", description="Plays a sound in the voice channel")
    @app_commands.describe(sound_name="The name of the sound to play")
    async def play(self, interaction: Interaction, sound_name: str):
        if sound_name is None:
            return await interaction.response.send_message(
                "Provide a sound name to play. Use /ls to see available sounds."
            )

        sounds = self.sounds_manager.update_sounds()

        if sound_name not in sounds:
            return await interaction.response.send_message(
                f"Sound '{sound_name}' not found."
            )

        voice_client: VoiceClient = interaction.guild.voice_client

        error = play_audio(sound_name, voice_client)

        if error:
            await interaction.response.send_message(error)
        await interaction.response.send_message(f"Playing sound: {sound_name}")

    @app_commands.command(name="stop", description="Stops playing the current sound")
    async def stop(self, interaction: Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            logger.info("Stopped playing sound")
            await interaction.response.send_message("Stopped playing sound.")
        else:
            logger.info("No sound is currently playing")
            await interaction.response.send_message("No sound is currently playing.")

    @app_commands.command(
        name="upload",
        description="Uploads a new sound (Owner only). The filename will be used as the sound key",
    )
    @app_commands.describe(attachment="A mp3 file")
    async def upload(self, interaction: Interaction, attachment: Attachment):
        if not attachment:
            return await interaction.response.send_message("Please upload a sound file")

        file_name = attachment.filename

        if not file_name.endswith(".mp3"):
            return await interaction.response.send_message(
                "Please upload a valid .mp3 file."
            )

        if attachment.content_type != "audio/mpeg":
            await interaction.response.send_message(
                f"Skipping {file_name}: not an MP3 audio file."
            )

        file_path = str(MP3_PATH / file_name)
        await attachment.save(fp=file_path)

        await interaction.response.send_message(
            f"Sound {file_name} uploaded successfully!"
        )

    @app_commands.command(name="remove", description="Removes a sound")
    @app_commands.describe(sound_name="The name of the sound to remove")
    async def remove(self, interaction: Interaction, sound_name: str):
        sounds = self.sounds_manager.update_sounds()
        if sound_name not in sounds:
            await interaction.response.send_message(
                f"Sound {sound_name} does not exist!"
            )
            return

        # Construct and validate the file path to prevent path traversal attacks
        file_path = (MP3_PATH / f"{sound_name}.mp3").resolve()

        # Ensure the resolved path is still within the MP3_PATH directory
        try:
            file_path.relative_to(MP3_PATH.resolve())
        except ValueError:
            logger.error(f"Attempt to access file outside mp3 directory: {sound_name}")
            await interaction.response.send_message("Invalid sound name!")
            return

        if file_path.exists():
            logger.info(f"Removing sound {sound_name}")
            os.remove(file_path)
            await interaction.response.send_message(f"Sound {sound_name} was removed")
        else:
            logger.error(f"Sound filepath `{file_path}` does not exist!")
            await interaction.response.send_message(
                f"Could not remove sound {sound_name}"
            )

    @play.autocomplete("sound_name")
    @remove.autocomplete("sound_name")
    async def sound_name_autocomplete(
        self, interaction: Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        """
        Autocomplete handler for sound names. Returns the top 25 sound names that match the current input.

        :param self: The instance of the class
        :param interaction: The Discord Interaction
        :type interaction: Interaction
        :param current: The current input from the user
        :type current: str
        :return: A list of autocomplete choices
        :rtype: List[Choice[str]]
        """
        return self.sounds_manager.sound_autocomplete(current)
