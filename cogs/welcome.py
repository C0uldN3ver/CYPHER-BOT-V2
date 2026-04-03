# cogs/welcome.py - MASTER VERSION
import discord
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

# --- Configuration from Environment Variables ---
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("✅ Welcome cog initialized.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends an automated welcome message to new members."""
        if member.bot:
            return

        if not WELCOME_CHANNEL_ID:
            logger.warning("WELCOME_CHANNEL_ID is not set. Skipping welcome message.")
            return

        welcome_channel = self.bot.get_channel(int(WELCOME_CHANNEL_ID))
        if not welcome_channel:
            logger.error(f"❌ Welcome channel with ID {WELCOME_CHANNEL_ID} not found.")
            return

        try:
            embed = discord.Embed(
                title=f"🎉 Welcome to the Cypher Assets Collective, {member.name}!",
                description=(
                    f"We're thrilled to have you join our community of disciplined traders. "
                    f"To get started, please check out our rules and complete the verification process.\n\n"
                    f"We believe in **Precision. Discipline. Profit.** and look forward to your contributions!"
                ),
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")
            embed.timestamp = discord.utils.utcnow()

            await welcome_channel.send(f"Welcome {member.mention}!", embed=embed)
            logger.info(f"✅ Sent welcome message to {member.name} in {welcome_channel.name}.")
        except discord.Forbidden:
            logger.error(f"❌ Missing permissions to send messages in welcome channel.")
        except Exception as e:
            logger.error(f"❌ Error sending welcome message to {member.name}: {e}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
