# cogs/mentorship.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class Mentorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Mentorship cog initialized.")

    @app_commands.command(name="request_mentor", description="Request a mentor.")
    @app_commands.guilds(MY_GUILD)
    async def request_mentor(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🤝 Mentorship Request",
            description="Your mentorship request has been submitted. A mentor will contact you soon.",
            color=discord.Color.purple()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Mentorship request from {interaction.user.name}")

async def setup(bot):
    await bot.add_cog(Mentorship(bot))
