# cogs/moderation.py - MASTER VERSION
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

# --- Configuration from Environment Variables ---
MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))
OWNER_ROLE_ID = os.getenv("OWNER_ROLE_ID")

# --- Custom Check for Owner Role ---
def is_owner_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not OWNER_ROLE_ID:
            logger.warning("OWNER_ROLE_ID is not set. Owner check bypassed.")
            return True
        
        owner_role = interaction.guild.get_role(int(OWNER_ROLE_ID))
        if owner_role and owner_role in interaction.user.roles or interaction.user.id == interaction.guild.owner_id:
            return True
        await interaction.response.send_message("❌ This command is restricted to the **Owner** only.", ephemeral=True)
        return False
    return app_commands.check(predicate)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Moderation cog initialized.")

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.guilds(MY_GUILD)
    @is_owner_check()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await interaction.response.defer(ephemeral=True)
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="✅ Member Kicked",
                description=f"**Member:** {member.mention}\n**Reason:** {reason}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"Kicked {member.name} for reason: {reason}")
        except Exception as e:
            logger.error(f"Failed to kick {member.name}: {e}")
            await interaction.followup.send(f"❌ Failed to kick member: {e}", ephemeral=True)

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.guilds(MY_GUILD)
    @is_owner_check()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await interaction.response.defer(ephemeral=True)
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="✅ Member Banned",
                description=f"**Member:** {member.mention}\n**Reason:** {reason}",
                color=discord.Color.dark_red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"Banned {member.name} for reason: {reason}")
        except Exception as e:
            logger.error(f"Failed to ban {member.name}: {e}")
            await interaction.followup.send(f"❌ Failed to ban member: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
