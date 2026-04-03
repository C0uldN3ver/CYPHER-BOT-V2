# cogs/graduation.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class Graduation(commands.Cog):
    """Handles member graduation from the bootcamp program."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Graduation cog initialized.")

    @app_commands.command(name="graduate", description="Graduate a member from the bootcamp.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(manage_roles=True)
    async def graduate(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🎓 Member Graduated",
            description=(
                f"Congratulations {member.mention}! You have successfully graduated "
                f"from the Cypher Assets Bootcamp."
            ),
            color=discord.Color.gold(),
        )
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"{interaction.user.name} graduated {member.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Graduation(bot))
