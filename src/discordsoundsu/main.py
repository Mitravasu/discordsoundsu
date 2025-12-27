import os
import logging
import asyncio
import threading

from .client import DiscordSoundsUClient
from .api import SoundsAPI
from dotenv import load_dotenv
from uvicorn import Server, Config

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


async def initialize_bot() -> DiscordSoundsUClient:
    client = DiscordSoundsUClient()
    return await client.initialize()


def run_api(client: DiscordSoundsUClient):
    """Run the REST API in a separate thread"""
    logger.info("Starting REST API server")
    api = SoundsAPI(client.bot, client.sounds_manager)
    config = Config(app=api.app, host="0.0.0.0", port=8000, log_level="info")
    server = Server(config)
    asyncio.run(server.serve())


def main():
    logger.info("Starting DiscordSoundsU Bot")
    client = asyncio.run(initialize_bot())

    # Start API in a separate thread
    api_thread = threading.Thread(target=run_api, args=(client,), daemon=True)
    api_thread.start()

    logger.info("Running DiscordSoundsU Bot")
    client.bot.run(os.getenv("DISCORD_TOKEN"))
