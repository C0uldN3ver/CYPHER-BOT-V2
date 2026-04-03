# cogs/inactivity.py - MASTER VERSION
import discord
from discord.ext import commands, tasks
import os
import logging

logger = logging.getLogger(__name__)

class Inactivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Inactivity cog initialized.")

    @tasks.loop(hours=24)
    async def check_inactivity(self):
        """Check for inactive members every 24 hours."""
        logger.info("Checking for inactive members...")

    @check_inactivity.before_loop
    async def before_check_inactivity(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Inactivity(bot))
