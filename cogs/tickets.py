# cogs/tickets.py - MASTER VERSION
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging

logger = logging.getLogger(__name__)

MY_GUILD = discord.Object(id=int(os.getenv("GUILD_ID")))

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.primary, emoji="🎫", custom_id="create_ticket_button")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Ticket created! A support team member will assist you soon.", ephemeral=True)
        logger.info(f"Ticket created by {interaction.user.name}")

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(TicketView())
        logger.info("✅ Tickets cog initialized.")

    @app_commands.command(name="setup_tickets", description="Post the ticket creation panel.")
    @app_commands.guilds(MY_GUILD)
    async def setup_tickets(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(
            title="🎫 Support Tickets",
            description="Click the button below to create a support ticket.",
            color=discord.Color.blue()
        )
        await interaction.channel.send(embed=embed, view=TicketView())
        await interaction.followup.send("✅ Ticket panel posted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
