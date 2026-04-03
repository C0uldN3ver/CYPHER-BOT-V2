# cogs/verification.py - MASTER VERSION
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

# --- Configuration from Environment Variables ---
MEMBER_ROLE_ID = os.getenv("MEMBER_ROLE_ID")
UNVERIFIED_ROLE_ID = os.getenv("UNVERIFIED_ROLE_ID")
OWNER_ROLE_ID = os.getenv("OWNER_ROLE_ID")
GUILD_ID = int(os.getenv("GUILD_ID"))

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

# --- Views ---
class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="🏛️ Verify Access",
        style=discord.ButtonStyle.success,
        custom_id="verify_member_button"
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        member_role = guild.get_role(int(MEMBER_ROLE_ID)) if MEMBER_ROLE_ID else None
        unverified_role = guild.get_role(int(UNVERIFIED_ROLE_ID)) if UNVERIFIED_ROLE_ID else None
        
        if not member_role:
            logger.error(f"❌ MEMBER_ROLE_ID {MEMBER_ROLE_ID} not found in guild {guild.name}.")
            await interaction.followup.send("❌ Member role not found. Please contact an administrator.", ephemeral=True)
            return

        if member_role in interaction.user.roles:
            await interaction.followup.send("✅ You are already verified.", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(member_role)
            logger.info(f"Assigned Member role to {interaction.user.name} ({interaction.user.id}).")
            
            if unverified_role and unverified_role in interaction.user.roles:
                await interaction.user.remove_roles(unverified_role)
                logger.info(f"Removed Unverified role from {interaction.user.name} ({interaction.user.id}).")
                
            await interaction.followup.send(
                f"🏛️ **Access Granted, {interaction.user.mention}!**\n\n"
                "You have been successfully verified as a member of **Cypher Assets Collective**.\n"
                "Welcome to the inner circle. Precision. Discipline. Profit.",
                ephemeral=True
            )
        except discord.Forbidden:
            logger.error(f"❌ Missing permissions to manage roles for {interaction.user.name} in {guild.name}.")
            await interaction.followup.send(f"❌ Failed to update roles: Missing permissions.", ephemeral=True)
        except Exception as e:
            logger.error(f"❌ Failed to update roles for {interaction.user.name}: {e}")
            await interaction.followup.send(f"❌ Failed to update roles: An unexpected error occurred.", ephemeral=True)

# --- Cog Definition ---
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(VerificationView())
        logger.info("Verification cog initialized. Persistent VerificationView added.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Automatically assign the Unverified role when a new member joins."""
        if member.bot:
            return

        unverified_role = member.guild.get_role(int(UNVERIFIED_ROLE_ID)) if UNVERIFIED_ROLE_ID else None
        if unverified_role:
            try:
                await member.add_roles(unverified_role)
                logger.info(f"✅ Assigned Unverified role to new member {member.name} ({member.id}).")
            except discord.Forbidden:
                logger.error(f"❌ Missing permissions to assign Unverified role to {member.name} in {member.guild.name}.")
            except Exception as e:
                logger.error(f"❌ Failed to assign Unverified role to {member.name}: {e}")

    @app_commands.command(
        name="setup_verify_panel",
        description="Post the premium verification panel. (Owner only)"
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @is_owner_check()
    async def setup_verify_panel(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="𝐂𝐘𝐏𝐇𝐄𝐑 𝐀𝐒𝐒𝐄𝐓𝐒 — 𝐈𝐍𝐒𝐓𝐈𝐓𝐔𝐓𝐈𝐎𝐍𝐀𝐋 𝐕𝐄𝐑𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍",
            description=(
                "> **𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐓𝐇𝐄 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐕𝐄**\n"
                "> \n"
                "> You have reached the gateway of Cypher Assets. To gain access to our institutional "
                "trading environment, resources, and community, you must complete the verification "
                "process below.\n"
                "> \n"
                "> **🔹 𝐖𝐇𝐘 𝐕𝐄𝐑𝐈𝐅𝐘?**\n"
                "> \n"
                "> Our verification process ensures a secure and high-quality environment for all members. "
                "It helps us maintain the integrity of our collective and provides you with access to "
                "exclusive tools, insights, and a network of like-minded traders.\n"
                "> \n"
                "> **🔹 𝐇𝐎𝐖 𝐓𝐎 𝐕𝐄𝐑𝐈𝐅𝐘:**\n"
                "> \n"
                "> Simply click the `🏛️ Verify Access` button below. Upon successful verification, you will "
                "automatically receive the `Member` role and unlock full access to the server.\n"
                "> \n"
                "> **Precision. Discipline. Profit.** 🏛️\n"
                "> \n"
                "> — **𝐂𝐘𝐏𝐇𝐄𝐑 𝐀𝐒𝐒𝐄𝐓𝐒 𝐂𝐎𝐋𝐋𝐄𝐂𝐓𝐈𝐕𝐄** 🏛️"
            ),
            color=discord.Color.dark_gold()
        )
        embed.set_footer(text="Cypher Assets Collective • Institutional Standards")

        await interaction.channel.send(embed=embed, view=VerificationView())
        await interaction.followup.send("✅ Verification panel posted successfully.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Verification(bot))
