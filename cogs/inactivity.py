# cogs/inactivity.py - CYPHER-BOT V2
import discord
from discord.ext import commands, tasks
import logging

logger = logging.getLogger(__name__)


class Inactivity(commands.Cog):
    """Monitors member inactivity (placeholder — no action taken yet)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Start the background task loop
        self.check_inactivity.start()
        logger.info("Inactivity cog initialized. Background loop started.")

    def cog_unload(self):
        """Clean up the background task when the cog is unloaded."""
        self.check_inactivity.cancel()

    @tasks.loop(hours=24)
    async def check_inactivity(self):
        """Check for inactive members every 24 hours."""
        logger.info("Inactivity check running... (placeholder — no action taken)")

    @check_inactivity.before_loop
    async def before_check_inactivity(self):
        """Wait until the bot is fully ready before starting the loop."""
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(Inactivity(bot))
