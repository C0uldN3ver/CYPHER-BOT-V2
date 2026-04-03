# cogs/crypto_news.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class CryptoNews(commands.Cog):
    """Provides cryptocurrency news updates."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("CryptoNews cog initialized.")

    @app_commands.command(name="crypto_news", description="Get the latest cryptocurrency news.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def crypto_news(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(
            title="📰 Cryptocurrency News",
            description="Here are the latest cryptocurrency updates and market insights.",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Bitcoin", value="Latest BTC updates", inline=False)
        embed.add_field(name="Ethereum", value="Latest ETH updates", inline=False)
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
        await interaction.followup.send(embed=embed)
        logger.info(f"Crypto news requested by {interaction.user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(CryptoNews(bot))
