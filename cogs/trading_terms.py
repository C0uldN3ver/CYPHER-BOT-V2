# cogs/trading_terms.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
TRADING_TERMS_FILE = os.getenv("TRADING_TERMS_FILE", "data/trading_terms.json")

def load_trading_terms():
    """Loads trading terms from a JSON file."""
    if not os.path.exists(TRADING_TERMS_FILE):
        logger.warning(f"Trading terms file not found at {TRADING_TERMS_FILE}. Initializing with empty data.")
        return {}
    try:
        with open(TRADING_TERMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {TRADING_TERMS_FILE}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading trading terms from {TRADING_TERMS_FILE}: {e}")
        return {}

class TradingTerms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.terms = load_trading_terms()
        logger.info("✅ TradingTerms cog initialized.")

    @app_commands.command(name="term", description="Look up a trading term.")
    @app_commands.guilds(MY_GUILD)
    async def get_term(self, interaction: discord.Interaction, term: str):
        await interaction.response.defer(ephemeral=False)
        term_lower = term.lower()

        if term_lower in self.terms:
            definition = self.terms[term_lower]["definition"]
            example = self.terms[term_lower].get("example", "N/A")
            
            embed = discord.Embed(
                title=f"📚 Trading Term: {term.capitalize()}",
                description=definition,
                color=discord.Color.blue()
            )
            if example != "N/A":
                embed.add_field(name="Example", value=example, inline=False)
            embed.set_footer(text="Cypher Assets Collective")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"❌ Term '{term}' not found. Try another term or use `/list_terms`.", ephemeral=True)

    @app_commands.command(name="list_terms", description="List all available trading terms.")
    @app_commands.guilds(MY_GUILD)
    async def list_terms(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not self.terms:
            await interaction.followup.send("❌ No trading terms available yet.", ephemeral=True)
            return

        terms_list = sorted([term.capitalize() for term in self.terms.keys()])
        terms_str = ", ".join(terms_list[:20])  # Limit to first 20

        embed = discord.Embed(
            title="📚 Available Trading Terms",
            description=f"Here are the terms you can look up:\n\n{terms_str}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Cypher Assets Collective")
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TradingTerms(bot))
