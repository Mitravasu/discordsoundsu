"""
Commands related to sleep operations.

- Toggle Sleep Mode
- Schedule Sleep
"""

import logging
import asyncio

from discord.ext import tasks
from discord.ext.commands import Bot, Cog
from datetime import time
from zoneinfo import ZoneInfo
from discord import Interaction, app_commands

from ..utils import kick_all_from_vc, play_audio
from typing import List
from ..sounds_manager import SoundsManager

logger = logging.getLogger(__name__)


class SleepCommands(Cog):
    def __init__(self, bot: Bot, sounds_manager: SoundsManager):
        self.WAIT_TIME = 30

        self.bot = bot
        self.sleep_mode = False
        self.sleep_time = time(0, 0, tzinfo=ZoneInfo("America/New_York"))
        self.sleep_sound = "sleep"
        self.sounds_manager = sounds_manager

        @tasks.loop(time=self.sleep_time)  # time set dynamically later
        async def sleep_task():
            logger.info("Sleep task starting...")
            vc_to_use = next(
                (voice_client for voice_client in self.bot.voice_clients), None
            )

            if not vc_to_use:
                logger.info("No voice client connected. Joining vc with members")
                vc_to_use = next(
                    (
                        voice_channel
                        for guild in bot.guilds
                        for voice_channel in guild.voice_channels
                        if len(voice_channel.members) > 0
                    ),
                    None,
                )

                if vc_to_use:
                    await vc_to_use.connect()
                else:
                    logger.info(
                        "No voice channels with members found. Skipping sleep sound."
                    )
                    return

            logger.info("Playing sleep sound...")
            err = play_audio(self.sleep_sound, self.bot.voice_clients[0])
            if err:
                logger.error(f"Error playing sound {self.sleep_sound}")
            else:
                # Play the sleep sound for WAIT_TIME seconds
                await asyncio.sleep(self.WAIT_TIME)

            await kick_all_from_vc(self.bot.guilds)
            logger.info("Kicked all users from voice channels for sleep mode.")

        self.sleep_task = sleep_task

    @app_commands.command(name="toggle_sleep", description="Toggles the sleep mode")
    @app_commands.describe(sleep="Enable or disable sleep mode")
    async def join(self, interaction: Interaction, sleep: bool):
        self.sleep_mode = sleep

        if sleep:
            if self.sleep_task.is_running():
                logger.error("Sleep task is already running")
                await interaction.response.send_message("Sleep task is already ENABLED")
                return

            self.sleep_task.start()
        else:
            self.sleep_task.stop()

        sleep_status = "ENABLED" if sleep else "DISABLED"
        formatted_time = self.sleep_time.strftime("%H:%M")

        await interaction.response.send_message(
            f"Sleep mode: [{sleep_status}] | Time: {formatted_time}"
        )

    @app_commands.command(name="set_sleep", description="Set a daily sleep time.")
    @app_commands.describe(
        hour="What hour do you want to sleep (0-23)?",
        minute="What minute do you want to sleep (0-59)?",
    )
    async def set_sleep(
        self,
        interaction: Interaction,
        hour: app_commands.Range[int, 0, 23],
        minute: app_commands.Range[int, 0, 59],
    ):
        logger.info(f"Setting sleep time to {hour:02}:{minute:02}")
        self.sleep_time = time(hour, minute, tzinfo=ZoneInfo("America/New_York"))
        logger.info(f"Updated sleep time to {self.sleep_time}")
        self.sleep_task.change_interval(time=self.sleep_time)

        if not self.sleep_task.is_running():
            logger.info("Enabling Sleep Task")
            self.sleep_mode = True
            self.sleep_task.start()
        else:
            logger.info("Sleep task already running, updated time only")

        await interaction.response.send_message(
            f"Sleep time set to {hour:02}:{minute:02} daily."
        )

    @app_commands.command(name="view_sleep", description="View the current sleep time")
    async def view_sleep(self, interaction: Interaction):
        logger.info(f"Viewing current sleep time: {self.sleep_time}")
        formatted_time = self.sleep_time.strftime("%H:%M")

        await interaction.response.send_message(
            f"Sleep mode: [{self.sleep_mode}] | Time: {formatted_time} | Sleep Sound: {self.sleep_sound}"
        )

    @app_commands.command(name="set_sleep_sound", description="set the sleep sound")
    async def set_sleep_sound(self, interaction: Interaction, sound_name: str):
        if sound_name is None:
            return await interaction.response.send_message.send(
                "Provide a sound name to play. Use /ls to see available sounds."
            )
        sounds = self.sounds_manager.update_sounds()
        if sound_name not in sounds:
            return await interaction.response.send_message(
                f"Sound '{sound_name}' not found."
            )

        self.sleep_sound = sound_name

        await interaction.response.send_message(f"Sleep sound set as: {sound_name}")

    @set_sleep_sound.autocomplete("sound_name")
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
