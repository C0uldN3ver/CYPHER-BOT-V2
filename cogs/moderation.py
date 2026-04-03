# cogs/moderation.py - CYPHER-BOT V2
import discord
from discord import app_commands
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))
OWNER_ROLE_ID = os.getenv("OWNER_ROLE_ID")


def is_owner_check():
    """Custom check: only the guild owner or users with the Owner role can use this command."""
    async def predicate(interaction: discord.Interaction) -> bool:
        # Always allow the guild owner
        if interaction.user.id == interaction.guild.owner_id:
            return True

        # If OWNER_ROLE_ID is configured, check for the role
        if OWNER_ROLE_ID:
            try:
                owner_role = interaction.guild.get_role(int(OWNER_ROLE_ID))
                if owner_role and owner_role in interaction.user.roles:
                    return True
            except ValueError:
                logger.error(f"OWNER_ROLE_ID '{OWNER_ROLE_ID}' is not a valid integer.")

        await interaction.response.send_message(
            "❌ This command is restricted to the **Owner** only.", ephemeral=True
        )
        return False

    return app_commands.check(predicate)


class Moderation(commands.Cog):
    """Server moderation commands (kick, ban)."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        logger.info("Moderation cog initialized.")

    @app_commands.command(name="kick", description="Kick a member from the server.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(kick_members=True)
    @is_owner_check()
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="Member Kicked",
                description=f"**Member:** {member.mention}\n**Reason:** {reason}",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user.name} kicked {member.name} — Reason: {reason}")
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ I don't have permission to kick this member.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Failed to kick {member.name}: {e}")
            await interaction.followup.send(
                "❌ An error occurred while trying to kick this member.", ephemeral=True
            )

    @app_commands.command(name="ban", description="Ban a member from the server.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(ban_members=True)
    @is_owner_check()
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided",
    ):
        await interaction.response.defer(ephemeral=True)
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Member Banned",
                description=f"**Member:** {member.mention}\n**Reason:** {reason}",
                color=discord.Color.dark_red(),
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"{interaction.user.name} banned {member.name} — Reason: {reason}")
        except discord.Forbidden:
            await interaction.followup.send(
                "❌ I don't have permission to ban this member.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Failed to ban {member.name}: {e}")
            await interaction.followup.send(
                "❌ An error occurred while trying to ban this member.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
