# cogs/tickets.py - CYPHER-BOT V2
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))


class TicketView(discord.ui.View):
    """Persistent view with a button to create support tickets."""

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.primary,
        emoji="\U0001f3ab",
        custom_id="create_ticket_button",
    )
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "\u2705 Ticket created! A support team member will assist you soon.",
            ephemeral=True,
        )
        logger.info(f"Ticket created by {interaction.user.name}")


class Tickets(commands.Cog):
    """Support ticket system."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(TicketView())
        logger.info("Tickets cog initialized. Persistent TicketView registered.")

    @app_commands.command(name="setup_tickets", description="Post the ticket creation panel.")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(manage_channels=True)
    async def setup_tickets(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="\U0001f3ab Support Tickets",
            description="Click the button below to create a support ticket.",
            color=discord.Color.blue(),
        )
        embed.set_footer(text="Cypher Assets Collective")
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.followup.send("\u2705 Ticket panel posted.", ephemeral=True)
        logger.info(f"Ticket panel posted by {interaction.user.name}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot))
