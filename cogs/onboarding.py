# cogs/onboarding.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class Onboarding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Onboarding cog initialized.")

    @app_commands.command(name="onboard", description="Start the onboarding process.")
    @app_commands.guilds(MY_GUILD)
    async def onboard(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="👋 Welcome to Onboarding",
            description="Welcome to the Cypher Assets Collective! Let's get you started.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Onboarded {interaction.user.name}")

async def setup(bot):
    await bot.add_cog(Onboarding(bot))
