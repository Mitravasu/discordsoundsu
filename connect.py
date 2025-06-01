import os
import re
import discord
from discord.ext import commands
import discord.ext.commands
from dotenv import load_dotenv

import discord.ext

load_dotenv()

intents = discord.Intents.none()
intents.voice_states = True
intents.dm_messages = True
intents.guild_messages = True
intents.guilds = True
intents.message_content = True

client = commands.Bot(command_prefix=commands.when_mentioned_or("."), intents=intents)
soundMap = [os.path.splitext(f)[0] for f in os.listdir('./mp3') if f.endswith('.mp3')]

def extract_emoji_name(emoji_string):
    # Match any text between colons in a Discord emoji format
    pattern = r'<:([^:]+):\d+>'
    match = re.search(pattern, emoji_string)
    
    if match:
        return match.group(1)
    return emoji_string

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('.'):
        await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        return

    if before.channel is None and after.channel is not None:
        print(f'{member.name} joined {after.channel.name}')
    elif before.channel is not None and after.channel is None:
        print(f'{member.name} left {before.channel.name}')
    elif before.channel != after.channel:
        print(f'{member.name} moved from {before.channel.name} to {after.channel.name}')

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

@client.command()
async def joinvc(ctx, channel: discord.VoiceChannel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    
    await channel.connect()

@client.command()
async def leavevc(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not connected to a voice channel.")

@client.command()
async def play(ctx: discord.ext.commands.Context, emoji: str = None):
    if (emoji is None):
        return ctx.send("Please provide an emoji to play a sound.")
    
    emoji_name = extract_emoji_name(emoji)
    print(f"Emoji name extracted: {emoji_name}")

    if (emoji_name not in soundMap):
        return ctx.send(f"Sound for emoji '{emoji_name}' not found.")
    
    voice_client: discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return print("I'm not connected to a voice channel.")
    
    source = discord.FFmpegPCMAudio(f'mp3/{emoji_name}.mp3')

    if not source:
        return print(f"Could not load sound: {emoji_name}")
    
    if not voice_client.is_playing():
        print(f'Playing sound: {emoji_name}')
        def after_playing(error):
            if error:
                print(f'Error playing sound: {error}')
            print(f'Finished playing sound: {emoji_name}')
        voice_client.play(source, after=after_playing)
    else:
        print("Already playing a sound, cannot play another one right now.")



client.run(os.getenv('DISCORD_TOKEN'))