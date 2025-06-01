import os
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

@client.event
async def on_ready():
    print('Bot is ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('.'):
        await client.process_commands(message)

async def on_guild_message(message):
    if message.author.bot:
        return

    if message.content.startswith('.hello'):
        await message.channel.send('Hello!')

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
async def play(ctx: discord.ext.commands.Context):
    voice_client: discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return print("I'm not connected to a voice channel.")
    
    sounds = ctx.guild.soundboard_sounds

    if not sounds:
        return print("No sounds available to play.")
    
    sound = sounds[0]  # For simplicity, just play the first sound
    
    source = discord.FFmpegPCMAudio('sounds/tarabipbip.mp3')

    if not source:
        return print(f"Could not load sound: {sound.name}")
    
    if not voice_client.is_playing():
        print(f'Playing sound: {sound.name}')
        def after_playing(error):
            if error:
                print(f'Error playing sound: {error}')
            print(f'Finished playing sound: {sound.name}')
        voice_client.play(source, after=after_playing)
    else:
        print("Already playing a sound, cannot play another one right now.")



client.run(os.getenv('DISCORD_TOKEN'))