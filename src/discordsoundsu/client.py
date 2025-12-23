"""
DiscordSoundsU Client Module
"""

import logging

from discord import Intents, Member, VoiceState
from discord.ext.commands import Bot, when_mentioned_or
from .commands.vc import VoiceCommands
from .commands.owner import OwnerCommands
from .commands.sounds import SoundCommands
from .commands.sleep import SleepCommands

from .utils import play_audio
from .sounds_manager import SoundsManager

logger = logging.getLogger(__name__)


class DiscordSoundsUClient:
    def __init__(self):
        intents = Intents.none()
        intents.voice_states = True
        intents.dm_messages = True
        intents.guild_messages = True
        intents.guilds = True
        intents.message_content = True

        self.bot = Bot(command_prefix=when_mentioned_or("."), intents=intents)

        # Register event handlers
        self.bot.add_listener(self.on_ready)
        self.bot.add_listener(self.on_voice_state_update)

        self.sounds_manager = SoundsManager()

    async def initialize(self):
        logger.info("Initializing DiscordSoundsU Client...")
        await self._register_cogs()

        logger.info("DiscordSoundsU Client initialized!")
        return self

    async def _register_cogs(self):
        logger.info("Registering Cogs...")
        await self.bot.add_cog(VoiceCommands(self.bot))
        await self.bot.add_cog(OwnerCommands(self.bot))
        await self.bot.add_cog(SoundCommands(self.bot, self.sounds_manager))
        await self.bot.add_cog(SleepCommands(self.bot, self.sounds_manager))
        logger.info("Cogs registered!")

    # Event Handlers

    async def on_ready(self):
        logger.info("Bot is ready!")
        guild_to_join = [
            guild for guild in self.bot.guilds if guild.name == "Bestest Study Group"
        ][0]

        if not guild_to_join:
            logger.error("Did not find the guild to auto-join")
        else:
            vcs = [
                vc
                for vc in guild_to_join.voice_channels
                if vc.name == "games" and len(vc.members) > 0
            ]

            if vcs:
                logger.info(f"Joining vc {vcs[0].name}")
                await vcs[0].connect()
            else:
                logger.info("No vcs to join.")

    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member.bot:
            return

        # User joins a channel from nothing
        if before.channel is None and after.channel is not None:
            logger.info(f"{member.name} joined {after.channel.name}")

            if member.name in [".mx2", ".l3noire"] and len(self.bot.voice_clients) == 0:
                await after.channel.connect()

            # play welcome sound everytime a user joins a voice channel
            error = play_audio("welcome", after.channel.guild.voice_client)

            if error:
                logger.error(error)

        # User leaves a channel
        elif before.channel is not None and after.channel is None:
            logger.info(f"{member.name} left {before.channel.name}")

            if len(before.channel.members) == 1:
                logger.info(f"No members left in {before.channel.name}, disconnecting.")
                await self.bot.voice_clients[0].disconnect()
