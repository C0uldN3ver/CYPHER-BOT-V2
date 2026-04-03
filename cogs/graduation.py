# cogs/graduation.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class Graduation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Graduation cog initialized.")

    @app_commands.command(name="graduate", description="Graduate a member from the bootcamp.")
    @app_commands.guilds(MY_GUILD)
    async def graduate(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🎓 Member Graduated",
            description=f"Congratulations {member.mention}! You have successfully graduated from the Cypher Assets Bootcamp.",
            color=discord.Color.gold()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        logger.info(f"Graduated {member.name}")

async def setup(bot):
    await bot.add_cog(Graduation(bot))
