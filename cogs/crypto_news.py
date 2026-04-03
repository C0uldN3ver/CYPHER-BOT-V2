# cogs/crypto_news.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class CryptoNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Crypto News cog initialized.")

    @app_commands.command(name="crypto_news", description="Get the latest cryptocurrency news.")
    @app_commands.guilds(MY_GUILD)
    async def crypto_news(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        embed = discord.Embed(
            title="📰 Cryptocurrency News",
            description="Here are the latest cryptocurrency updates and market insights.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Bitcoin", value="Latest BTC updates", inline=False)
        embed.add_field(name="Ethereum", value="Latest ETH updates", inline=False)
        await interaction.followup.send(embed=embed)
        logger.info(f"Crypto news requested by {interaction.user.name}")

async def setup(bot):
    await bot.add_cog(CryptoNews(bot))
