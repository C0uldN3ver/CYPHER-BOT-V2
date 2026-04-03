# cogs/mentorship.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class Mentorship(commands.Cog):
    """Handles mentorship requests within the collective."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Mentorship cog initialized.")

    @app_commands.command(name="request_mentor", description="Request a mentor for trading guidance.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def request_mentor(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🧑‍🏫 Mentorship Request Submitted",
            description=(
                "Your mentorship request has been submitted. "
                "A senior trader will reach out to you soon."
            ),
            color=discord.Color.purple(),
        )
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Mentorship request from {interaction.user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Mentorship(bot))
