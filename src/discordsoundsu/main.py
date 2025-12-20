import os
import logging
import asyncio

from .client import DiscordSoundsUClient
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def initialize_bot() -> DiscordSoundsUClient:
    client = DiscordSoundsUClient()
    return await client.initialize()

def main():
    logger.info("Starting DiscordSoundsU Bot")
    client = asyncio.run(initialize_bot())

    logger.info("Running DiscordSoundsU Bot")
    client.bot.run(os.getenv("DISCORD_TOKEN"))
