"""
Commands related to owner-only functionalities.

- Sync Command Tree
"""

from discord.ext.commands import Bot, Cog, command, is_owner, Context


class OwnerCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="sync", help="Sync command tree with Discord")
    @is_owner()
    async def sync(self, ctx: Context):
        await self.bot.tree.sync()
        await ctx.send("Command tree synced with Discord.")
