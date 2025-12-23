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

logger = logging.getLogger(__name__)

class SleepCommands(Cog):
    def __init__(self, bot: Bot):
        self.WAIT_TIME = 30

        self.bot = bot
        self.sleep_mode = False
        self.sleep_time = time(0, 0, tzinfo=ZoneInfo("America/New_York"))
        self.sleep_sound = "sleep"

        @tasks.loop(time=self.sleep_time)  # time set dynamically later
        async def sleep_task():
            logger.info("Sleep task starting...")
            vc_to_use = next((voice_client for voice_client in self.bot.voice_clients), None)

            if not vc_to_use:
                logger.info("No voice client connected. Joining vc with members")
                vc_to_use = next((
                    voice_channel
                    for guild in bot.guilds
                    for voice_channel in guild.voice_channels
                    if len(voice_channel.members) > 0
                ), None)

                if vc_to_use:
                    await vc_to_use.connect()
                else:
                    logger.info("No voice channels with members found. Skipping sleep sound.")
                    return

            logger.info("Playing sleep sound...")
            play_audio(self.sleep_sound, self.bot.voice_clients[0])

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
        formatted_time = self.sleep_time.strftime('%H:%M')
                    
        await interaction.response.send_message(f"Sleep mode: [{sleep_status}] | Time: {formatted_time}")


    @app_commands.command(name="set_sleep", description="Set a daily sleep time.")
    @app_commands.describe(hour="What hour do you want to sleep (0-23)?", minute="What minute do you want to sleep (0-59)?")
    async def set_sleep(self, interaction: Interaction, hour: app_commands.Range[int, 0, 23], minute: app_commands.Range[int, 0, 59]):
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

        await interaction.response.send_message(f"Sleep time set to {hour:02}:{minute:02} daily.")