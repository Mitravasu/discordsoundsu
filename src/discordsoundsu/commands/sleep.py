"""
Commands related to sleep operations.

- Toggle Sleep Mode
- Schedule Sleep
"""

import logging
import asyncio

from typing import List
from discord.ext import tasks
from discord.ext.commands import Bot, Cog
from datetime import time
from zoneinfo import ZoneInfo, available_timezones
from discord import Interaction, app_commands

from ..utils import kick_all_from_vc, play_audio
from ..sounds_manager import SoundsManager
from ..ui.sleep_info_card import SleepInfoCard
from ..types import SleepData

logger = logging.getLogger(__name__)


class SleepCommands(Cog):
    def __init__(self, bot: Bot, sounds_manager: SoundsManager):
        self.bot = bot
        self.sleep_data = SleepData(timezone=ZoneInfo("America/New_York"), time=time(0, 0, tzinfo=ZoneInfo("America/New_York")), sound="sleep", is_enabled=False)
        self.sounds_manager = sounds_manager

        @tasks.loop(time=self.sleep_data.time)  # time set dynamically later
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
            err = play_audio(self.sleep_data.sound, self.bot.voice_clients[0])
            if err:
                logger.error(f"Error playing sound {self.sleep_data.sound}")
            else:
                # Play the sleep sound for WAIT_TIME seconds
                wait_time = self.sounds_manager.get_sound_duration(self.sleep_data.sound)
                await asyncio.sleep(wait_time)

            await kick_all_from_vc(self.bot.guilds)
            logger.info("Kicked all users from voice channels for sleep mode.")

        self.sleep_task = sleep_task

    @app_commands.command(name="toggle_sleep", description="Toggles the sleep mode")
    @app_commands.describe(sleep="Enable or disable sleep mode")
    async def toggle_sleep(self, interaction: Interaction, sleep: bool):
        if sleep and not self.sleep_task.is_running():
            logger.info("Enabling Sleep Task")
            self.sleep_task.start()
        elif not sleep and self.sleep_task.is_running():
            logger.info("Disabling Sleep Task")
            self.sleep_task.cancel()
        else:
            logger.info("Sleep Task already in desired state, no action taken")

        self.sleep_data.is_enabled = sleep

        await interaction.response.send_message(
            view=SleepInfoCard(self.sleep_data)
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
        self.sleep_data.time = time(hour, minute, tzinfo=self.sleep_data.timezone)
        logger.info(f"Updated sleep time to {self.sleep_data.time}")
        self.sleep_task.change_interval(time=self.sleep_data.time)

        if not self.sleep_task.is_running():
            self.sleep_task.start()
        else:
            self.sleep_task.restart()

        self.sleep_data.is_enabled = self.sleep_task.is_running()

        await interaction.response.send_message(
            view=SleepInfoCard(self.sleep_data)
        )

    @app_commands.command(name="view_sleep", description="View the current sleep time")
    async def view_sleep(self, interaction: Interaction):
        logger.info(f"Viewing current sleep time: {self.sleep_data.time}")
        self.sleep_data.is_enabled = self.sleep_task.is_running()

        await interaction.response.send_message(
            view=SleepInfoCard(self.sleep_data)
        )

    @app_commands.command(name="set_sleep_sound", description="Set the sleep sound")
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

        self.sleep_data.sound = sound_name

        await interaction.response.send_message(f"Sleep sound set as: {sound_name}")

    @app_commands.command(name="set_sleep_timezone", description="Set the sleep timezone")
    @app_commands.describe(
        timezone="The timezone to set for sleep scheduling (e.g., 'America/New_York')"
    )
    async def set_sleep_timezone(self, interaction: Interaction, timezone: str):
        try:
            self.sleep_data.timezone = ZoneInfo(timezone)
            # Update sleep_time with new timezone
            self.sleep_data.time = self.sleep_data.time.replace(tzinfo=self.sleep_data.timezone)
            # Update the task interval
            self.sleep_task.change_interval(time=self.sleep_data.time)

            # Restart the task if it's running to apply changes
            if self.sleep_task.is_running():
                self.sleep_task.restart()

            await interaction.response.send_message(
                f"Sleep timezone set to: {timezone}"
            )
        except Exception as error:
            logger.error(f"Error setting timezone: {error}")
            await interaction.response.send_message(
                f"Error setting timezone: {error}"
            )

    @set_sleep_timezone.autocomplete("timezone")
    async def sleep_timezone_autocomplete(
        self, interaction: Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        """
        Autocomplete handler for timezones. Returns the top 25 timezones that match the current input.

        :param self: The instance of the class
        :param interaction: The Discord Interaction
        :type interaction: Interaction
        :param current: The current input from the user
        :type current: str
        :return: A list of autocomplete choices
        :rtype: List[Choice[str]]
        """
        return [
            app_commands.Choice(name=tz, value=tz)
            for tz in sorted(available_timezones())
            if current.lower() in tz.lower()
        ][:25]

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
