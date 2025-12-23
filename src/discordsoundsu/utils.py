"""
A module for utility functions and classes for DiscordSoundsU.
"""
import re
import logging
import os
from pathlib import Path
from discord import FFmpegPCMAudio, VoiceClient, Guild

MP3_PATH = Path(__file__).parent.parent.parent / "mp3" 
logger = logging.getLogger(__name__)

def extract_emoji_name(emoji_string):
    # Match any text between colons in a Discord emoji format
    pattern = r'<:([^:]+):\d+>'
    match = re.search(pattern, emoji_string)
    
    if match:
        return match.group(1)
    return emoji_string

def fetch_sounds():
    return [os.path.splitext(f)[0] for f in os.listdir(MP3_PATH) if f.endswith('.mp3')]

def play_audio(file_name, voice_client: VoiceClient) -> None | str:
    """
    Plays an audio file in the connected voice channel.
    
    :param file_name: Name of the audio file (without extension)
    :param voice_client: Discord VoiceClient instance
    :return: None if successful, error message string otherwise
    :rtype: str | None
    """
    if not voice_client or not voice_client.is_connected():
        logger.error("Not connected to a voice channel.")
        return "Not connected to a voice channel."

    source = FFmpegPCMAudio(str(MP3_PATH / f"{file_name}.mp3"))

    if not source:
        logger.error(f"Could not load sound: {file_name}")
        return f"Could not load sound: {file_name}"

    if not voice_client.is_playing():
        logger.info(f'Playing sound: {file_name}')
        def after_playing(error):
            if error:
                logger.error(f'Error playing sound: {error}')
                return f'Error playing sound: {error}'
            logger.info(f'Finished playing sound: {file_name}')

        voice_client.play(source, after=after_playing)
    else:
        logger.error("Already playing a sound, cannot play another one right now.")
        return "Already playing a sound, cannot play another one right now."
    

async def kick_all_from_vc(guilds: list[Guild]):
    """Disconnect all users from voice channels"""
    members_to_kick = [
        member
        for guild in guilds
        for voice_channel in guild.voice_channels
        for member in voice_channel.members
        if not member.bot  # Don't kick bots
    ]

    for member in members_to_kick:
        try:
            await member.move_to(None)
            logger.info(f"Kicked {member.name} from voice channel")
        except Exception as e:
            logger.error(f"Failed to kick {member.name}: {e}")
