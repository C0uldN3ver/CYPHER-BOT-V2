# cogs/welcome.py - CYPHER-BOT V2
import discord
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")


class Welcome(commands.Cog):
    """Sends automated welcome messages to new members."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if not WELCOME_CHANNEL_ID:
            logger.warning("WELCOME_CHANNEL_ID is not set. Welcome messages will be disabled.")
        logger.info("Welcome cog initialized.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends a welcome message when a new member joins."""
        if member.bot:
            return

        if not WELCOME_CHANNEL_ID:
            return

        try:
            channel_id = int(WELCOME_CHANNEL_ID)
        except ValueError:
            logger.error(f"WELCOME_CHANNEL_ID '{WELCOME_CHANNEL_ID}' is not a valid integer.")
            return

        welcome_channel = self.bot.get_channel(channel_id)
        if not welcome_channel:
            logger.error(f"Welcome channel (ID: {channel_id}) not found.")
            return

        try:
            embed = discord.Embed(
                title=f"Welcome to the Cypher Assets Collective, {member.name}!",
                description=(
                    "We\'re thrilled to have you join our community of disciplined traders. "
                    "To get started, please check out our rules and complete the verification process.\n\n"
                    "We believe in **Precision. Discipline. Profit.** and look forward to your contributions!"
                ),
                color=discord.Color.green(),
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text="Cypher Assets Collective")
            embed.timestamp = discord.utils.utcnow()

            await welcome_channel.send(f"Welcome {member.mention}!", embed=embed)
            logger.info(f"Sent welcome message to {member.name}.")
        except discord.Forbidden:
            logger.error("Missing permissions to send messages in welcome channel.")
        except Exception as e:
            logger.error(f"Error sending welcome message to {member.name}: {e}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
