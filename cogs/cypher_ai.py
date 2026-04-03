# cogs/cypher_ai.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class CypherAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Cypher AI cog initialized.")

    @app_commands.command(name="ask_ai", description="Ask Cypher AI a question.")
    @app_commands.guilds(MY_GUILD)
    async def ask_ai(self, interaction: discord.Interaction, question: str):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🤖 Cypher AI Response",
            description=f"**Question:** {question}\n\n**Response:** I'm here to assist you with trading insights and guidance.",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"AI question from {interaction.user.name}: {question}")

async def setup(bot):
    await bot.add_cog(CypherAI(bot))
