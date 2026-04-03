# cogs/trading_terms.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


def _get_terms_path():
    """Get the absolute path to the trading terms JSON file."""
    # Use the directory of this file as the base, go up one level, then into data/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data", "trading_terms.json")


def load_trading_terms():
    """Loads trading terms from the JSON file."""
    path = _get_terms_path()
    if not os.path.exists(path):
        logger.warning(f"Trading terms file not found at {path}. Using empty data.")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error loading trading terms: {e}")
        return {}


class TradingTerms(commands.Cog):
    """Look up trading terminology."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.terms = load_trading_terms()
        logger.info(f"TradingTerms cog initialized. {len(self.terms)} terms loaded.")

    @app_commands.command(name="term", description="Look up a trading term.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def get_term(self, interaction: discord.Interaction, term: str):
        await interaction.response.defer(ephemeral=False)
        term_lower = term.lower()

        if term_lower in self.terms:
            definition = self.terms[term_lower]["definition"]
            example = self.terms[term_lower].get("example", "N/A")

            embed = discord.Embed(
                title=f"Trading Term: {term.capitalize()}",
                description=definition,
                color=discord.Color.blue(),
            )
            if example != "N/A":
                embed.add_field(name="Example", value=example, inline=False)
            embed.set_footer(text="Cypher Assets Collective")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"\u274c Term \'{term}\' not found. Try another term or use `/list_terms`.",
                ephemeral=True,
            )

    @app_commands.command(name="list_terms", description="List all available trading terms.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def list_terms(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        if not self.terms:
            await interaction.followup.send(
                "\u274c No trading terms available yet.", ephemeral=True
            )
            return

        terms_list = sorted([t.capitalize() for t in self.terms.keys()])
        terms_str = ", ".join(terms_list)

        embed = discord.Embed(
            title="Available Trading Terms",
            description=f"Here are the terms you can look up:\n\n{terms_str}",
            color=discord.Color.green(),
        )
        embed.set_footer(text="Cypher Assets Collective")
        await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(TradingTerms(bot))
