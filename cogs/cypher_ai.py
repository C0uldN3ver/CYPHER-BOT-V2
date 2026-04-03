# cogs/cypher_ai.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class CypherAI(commands.Cog):
    """Provides AI-powered trading assistance."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("CypherAI cog initialized.")

    @app_commands.command(name="ask_ai", description="Ask Cypher AI a question.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def ask_ai(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🤖 Cypher AI Response",
            description=(
                f"**Question:** {question}\n\n"
                f"**Response:** I'm here to assist you with trading insights and guidance."
            ),
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"AI question from {interaction.user.name}: {question[:50]}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CypherAI(bot))
