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
soundMap = []

def update_sound_map():
    global soundMap
    soundMap = [os.path.splitext(f)[0] for f in os.listdir('./mp3') if f.endswith('.mp3')]
    print(f"Sound map updated: {soundMap}")


def extract_emoji_name(emoji_string):
    # Match any text between colons in a Discord emoji format
    pattern = r'<:([^:]+):\d+>'
    match = re.search(pattern, emoji_string)
    
    if match:
        return match.group(1)
    return emoji_string

async def play_audio(file_name, voice_client):
    if not voice_client.is_connected():
        print("Not connected to a voice channel.")
        return
    
    source = discord.FFmpegPCMAudio(f'mp3/{file_name}.mp3')
    
    if not source:
        print(f"Could not load sound: {file_name}")
        return
    
    if not voice_client.is_playing():
        print(f'Playing sound: {file_name}')
        def after_playing(error):
            if error:
                print(f'Error playing sound: {error}')
            print(f'Finished playing sound: {file_name}')
        voice_client.play(source, after=after_playing)
    else:
        print("Already playing a sound, cannot play another one right now.")

@client.event
async def on_ready():
    print('Bot is ready!')
    update_sound_map()
    for guild in client.guilds:
        if guild.name == 'Bestest Study Group':
            for vc in guild.voice_channels:
                if vc.name == 'games' and len(vc.members) > 0:
                    print(f'Joining voice channel: {vc.name}')
                    await vc.connect()
                    break


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    command_word = message.content.split()[0].lower()
    
    if command_word == 'join':
        message.content = '.joinvc games'
        return await client.process_commands(message)
    elif command_word == 'leave':
        message.content = '.leavevc'
        return await client.process_commands(message)
    elif extract_emoji_name(command_word) in soundMap:
        message.content = f'.play {command_word}'
        return await client.process_commands(message)
    elif command_word == 'ls':
        message.content = '.ls'
        update_sound_map()
        return await client.process_commands(message)
    elif command_word.startswith('.'):
        if command_word == '.ls':
            update_sound_map()
        return await client.process_commands(message)
    elif command_word == 'upload':
        message.content = '.upload'
        return await client.process_commands(message)

@client.command()
async def upload(ctx: discord.ext.commands.Context):
    if not ctx.message.attachments:
        return await ctx.send("Please upload a sound file.")
    
    attachment = ctx.message.attachments[0]
    
    if not attachment.filename.endswith('.mp3'):
        return await ctx.send("Please upload a valid .mp3 file.")

    if attachment.content_type != "audio/mpeg":
        await ctx.send(f"Skipping {attachment.filename}: not an MP3 audio file.")

    file_name = attachment.filename
    file_path = os.path.join('mp3', file_name)
    await attachment.save(fp=file_path)

    update_sound_map()
    await ctx.send(f'Sound {file_name} uploaded successfully!')

@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.bot:
        return

    if before.channel is None and after.channel is not None:
        print(f'{member.name} joined {after.channel.name}')
        if member.name == '.mx2' or member.name == '.l3noire' and len(client.voice_clients) == 0:
            await after.channel.connect();
        # play welcome sound everytime a user joins a voice channel
        await play_audio('welcome', after.channel.guild.voice_client)
    elif before.channel is not None and after.channel is None:
        print(f'{member.name} left {before.channel.name}')
        if len(before.channel.members) == 1:
            print(f'No members left in {before.channel.name}, disconnecting.')
            await client.voice_clients[0].disconnect()

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
async def ls(ctx):
    if not soundMap:
        return await ctx.send("No sounds available.")
    
    sound_list = '\n'.join(soundMap)
    await ctx.send(f"Available sounds:\n```\n{sound_list}\n```")

@client.command()
async def play(ctx: discord.ext.commands.Context, emoji: str = None):
    if (emoji is None):
        return ctx.send("Please provide an emoji to play a sound.")
    
    emoji_name = extract_emoji_name(emoji)
    print(f"Emoji name extracted: {emoji_name}")

    if (emoji_name not in soundMap):
        return ctx.send(f"Sound for emoji '{emoji_name}' not found.")
    
    voice_client: discord.VoiceClient = ctx.voice_client

    await play_audio(emoji_name, voice_client)



client.run(os.getenv('DISCORD_TOKEN'))