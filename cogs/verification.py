# cogs/verification.py - CYPHER-BOT V2
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))
MEMBER_ROLE_ID = os.getenv("MEMBER_ROLE_ID")
UNVERIFIED_ROLE_ID = os.getenv("UNVERIFIED_ROLE_ID")
OWNER_ROLE_ID = os.getenv("OWNER_ROLE_ID")


def is_owner_check():
    """Custom check: only the guild owner or users with the Owner role can use this command."""
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id == interaction.guild.owner_id:
            return True
        if OWNER_ROLE_ID:
            try:
                owner_role = interaction.guild.get_role(int(OWNER_ROLE_ID))
                if owner_role and owner_role in interaction.user.roles:
                    return True
            except ValueError:
                logger.error(f"OWNER_ROLE_ID '{OWNER_ROLE_ID}' is not a valid integer.")
        await interaction.response.send_message(
            "\u274c This command is restricted to the **Owner** only.", ephemeral=True
        )
        return False
    return app_commands.check(predicate)


class VerificationView(discord.ui.View):
    """Persistent view with a verification button."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Verify Access",
        style=discord.ButtonStyle.success,
        emoji="\U0001f3db\ufe0f",
        custom_id="verify_member_button",
    )
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild

        # Get member role
        member_role = None
        if MEMBER_ROLE_ID:
            try:
                member_role = guild.get_role(int(MEMBER_ROLE_ID))
            except ValueError:
                logger.error(f"MEMBER_ROLE_ID '{MEMBER_ROLE_ID}' is not a valid integer.")

        if not member_role:
            logger.error(f"Member role not found (ID: {MEMBER_ROLE_ID}).")
            await interaction.followup.send(
                "\u274c Member role not found. Please contact an administrator.",
                ephemeral=True,
            )
            return

        if member_role in interaction.user.roles:
            await interaction.followup.send("\u2705 You are already verified.", ephemeral=True)
            return

        # Get unverified role (optional)
        unverified_role = None
        if UNVERIFIED_ROLE_ID:
            try:
                unverified_role = guild.get_role(int(UNVERIFIED_ROLE_ID))
            except ValueError:
                logger.error(f"UNVERIFIED_ROLE_ID '{UNVERIFIED_ROLE_ID}' is not a valid integer.")

        try:
            await interaction.user.add_roles(member_role)
            logger.info(f"Assigned Member role to {interaction.user.name} ({interaction.user.id}).")

            if unverified_role and unverified_role in interaction.user.roles:
                await interaction.user.remove_roles(unverified_role)
                logger.info(f"Removed Unverified role from {interaction.user.name}.")

            await interaction.followup.send(
                f"**Access Granted, {interaction.user.mention}!**\n\n"
                "You have been successfully verified as a member of **Cypher Assets Collective**.\n"
                "Welcome to the inner circle. Precision. Discipline. Profit.",
                ephemeral=True,
            )
        except discord.Forbidden:
            logger.error(f"Missing permissions to manage roles for {interaction.user.name}.")
            await interaction.followup.send(
                "\u274c Failed to update roles: Missing permissions.", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Failed to update roles for {interaction.user.name}: {e}")
            await interaction.followup.send(
                "\u274c Failed to update roles: An unexpected error occurred.",
                ephemeral=True,
            )


class Verification(commands.Cog):
    """Member verification system."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(VerificationView())
        logger.info("Verification cog initialized. Persistent VerificationView registered.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Automatically assign the Unverified role when a new member joins."""
        if member.bot:
            return

        if not UNVERIFIED_ROLE_ID:
            return

        try:
            unverified_role = member.guild.get_role(int(UNVERIFIED_ROLE_ID))
        except ValueError:
            logger.error(f"UNVERIFIED_ROLE_ID '{UNVERIFIED_ROLE_ID}' is not a valid integer.")
            return

        if not unverified_role:
            logger.warning(f"Unverified role (ID: {UNVERIFIED_ROLE_ID}) not found in guild.")
            return

        try:
            await member.add_roles(unverified_role)
            logger.info(f"Assigned Unverified role to new member {member.name} ({member.id}).")
        except discord.Forbidden:
            logger.error(f"Missing permissions to assign Unverified role to {member.name}.")
        except Exception as e:
            logger.error(f"Failed to assign Unverified role to {member.name}: {e}")

    @app_commands.command(
        name="setup_verify_panel",
        description="Post the verification panel. (Owner only)",
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    @is_owner_check()
    async def setup_verify_panel(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="CYPHER ASSETS \u2014 INSTITUTIONAL VERIFICATION",
            description=(
                "> **WELCOME TO THE COLLECTIVE**\n"
                "> \n"
                "> You have reached the gateway of Cypher Assets. To gain access to our "
                "institutional trading environment, resources, and community, you must "
                "complete the verification process below.\n"
                "> \n"
                "> **WHY VERIFY?**\n"
                "> \n"
                "> Our verification process ensures a secure and high-quality environment "
                "for all members. It helps us maintain the integrity of our collective and "
                "provides you with access to exclusive tools, insights, and a network of "
                "like-minded traders.\n"
                "> \n"
                "> **HOW TO VERIFY:**\n"
                "> \n"
                "> Simply click the `Verify Access` button below. Upon successful "
                "verification, you will automatically receive the `Member` role and unlock "
                "full access to the server.\n"
                "> \n"
                "> **Precision. Discipline. Profit.**\n"
                "> \n"
                "> \u2014 **CYPHER ASSETS COLLECTIVE**"
            ),
            color=discord.Color.dark_gold(),
        )
        embed.set_footer(text="Cypher Assets Collective \u2022 Institutional Standards")

        await interaction.channel.send(embed=embed, view=VerificationView())
        await interaction.followup.send("\u2705 Verification panel posted successfully.", ephemeral=True)
        logger.info(f"Verification panel posted by {interaction.user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Verification(bot))
