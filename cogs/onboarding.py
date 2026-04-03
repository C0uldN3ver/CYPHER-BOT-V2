# cogs/onboarding.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class Onboarding(commands.Cog):
    """Handles the onboarding process for new members."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Onboarding cog initialized.")

    @app_commands.command(name="onboard", description="Start the onboarding process.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def onboard(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="👋 Welcome to Onboarding",
            description=(
                "Welcome to the Cypher Assets Collective! Let's get you started.\n\n"
                "Please complete the verification process to gain full access to the server."
            ),
            color=discord.Color.green(),
        )
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Onboarding started for {interaction.user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Onboarding(bot))
