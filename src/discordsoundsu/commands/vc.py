"""
Commands related to voice channel operations.

- Join VC
- Leave VC
- Kick all from VC
"""
from discord.ext.commands import Bot, Cog
from discord import VoiceChannel, Interaction, app_commands


class VoiceCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @app_commands.command(name="join", description="Joins the specified voice channel")
    @app_commands.describe(channel="The voice channel to join")
    async def join(self, interaction: Interaction, channel: VoiceChannel):
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.move_to(channel)
            await interaction.response.send_message(f"Moved to {channel.name}")
        else:
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel.name}")

    @app_commands.command(name="leave", description="Leave the current voice channel")
    async def leave(self, interaction: Interaction):
        if interaction.guild.voice_client is not None:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Disconnected from voice channel")
        else:
            await interaction.response.send_message("I'm not connected to a voice channel.")