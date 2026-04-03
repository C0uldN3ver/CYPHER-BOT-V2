# cogs/tools.py - MASTER VERSION (Risk Calculator)
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging
from datetime import datetime, timezone

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

# --- Modals ---
class RiskCalculatorModal(ui.Modal, title="📊 CYPHER ASSET — RISK CALCULATOR"):
    balance = ui.TextInput(
        label="Account Balance ($)",
        placeholder="e.g. 100000",
        min_length=1,
        max_length=15,
        required=True
    )
    risk_pct = ui.TextInput(
        label="Risk Percentage (%)",
        placeholder="e.g. 0.5 or 1",
        min_length=1,
        max_length=5,
        required=True
    )
    entry_price = ui.TextInput(
        label="Entry Price",
        placeholder="e.g. 1.08500",
        min_length=1,
        max_length=15,
        required=True
    )
    sl_price = ui.TextInput(
        label="Stop-Loss Price",
        placeholder="e.g. 1.08350",
        min_length=1,
        max_length=15,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            # Input sanitization and conversion
            bal = float(self.balance.value.replace(",", ""))
            risk = float(self.risk_pct.value)
            entry = float(self.entry_price.value)
            sl_val = float(self.sl_price.value)

            if bal <= 0:
                raise ValueError("Account Balance must be positive.")
            if not (0 < risk <= 100):
                raise ValueError("Risk Percentage must be between 0 and 100.")
            if entry <= 0 or sl_val <= 0:
                raise ValueError("Entry Price and Stop-Loss Price must be positive.")

            # Calculate pip distance
            is_jpy = entry > 50 or sl_val > 50
            pip_multiplier = 100 if is_jpy else 10000
            
            pip_distance = abs(entry - sl_val) * pip_multiplier
            
            if pip_distance <= 0:
                raise ValueError("Entry Price and Stop-Loss Price cannot be the same.")

            # Standard calculation for Forex
            risk_amount = bal * (risk / 100)
            lot_size = risk_amount / (pip_distance * 10)

            embed = discord.Embed(
                title="📊 𝐂𝐘𝐏𝐇𝐄𝐑 𝐀𝐒𝐒𝐄𝐓𝐒 — 𝐑𝐈𝐒𝐊 𝐂𝐀𝐋𝐂𝐔𝐋𝐀𝐓𝐎𝐑",
                color=0xFFD700,
                timestamp=datetime.now(timezone.utc)
            )
            
            embed.add_field(
                name="***ACCOUNT PARAMETERS:***",
                value=(
                    f"> • Balance: **${bal:,.2f}**\n"
                    f"> • Risk Percentage: **{risk:.2f}%**\n"
                    f"> • Entry Price: **{entry:.5f}**\n"
                    f"> • Stop-Loss Price: **{sl_val:.5f}**"
                ),
                inline=False
            )
            
            embed.add_field(
                name="***EXECUTION DETAILS:***",
                value=(
                    f"> • **Pip Distance:** **{pip_distance:.1f} Pips**\n"
                    f"> • **Amount at Risk:** **${risk_amount:,.2f}**\n"
                    f"> • **Recommended Lot Size:** **{lot_size:.2f} Lots**"
                ),
                inline=False
            )
            
            embed.add_field(
                name="\u200b",
                value=(
                    "> *Capital protection is the first step to profitability. Ensure your entry aligns with the Cypher Protocol before execution. Never over-leverage based on emotion.*"
                ),
                inline=False
            )
            
            embed.set_footer(text="Cypher Assets Collective • Institutional Standards 🏛️")

            await interaction.followup.send(embed=embed, ephemeral=True)

        except ValueError as e:
            logger.error(f"Risk Calculator Input Error: {e}")
            await interaction.followup.send(
                f"❌ **Invalid Input.** {str(e)} Please ensure you enter valid numeric values.",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred in Risk Calculator: {e}")
            await interaction.followup.send("❌ An unexpected error occurred. Please try again later.", ephemeral=True)

# --- Views ---
class RiskCalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Calculate Position Size",
        style=discord.ButtonStyle.primary,
        emoji="📊",
        custom_id="calculate_risk_button"
    )
    async def calculate_risk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RiskCalculatorModal())

# --- Cog Definition ---
class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(RiskCalculatorView())
        logger.info("Tools cog (Risk Calculator) initialized. Persistent RiskCalculatorView added.")

    @app_commands.command(
        name="setup_risk_calculator",
        description="[ADMIN] Post the Risk Calculator panel in the current channel. (Owner only)"
    )
    @app_commands.guilds(MY_GUILD)
    @is_owner_check()
    async def setup_risk_calculator(self, interaction: discord.Interaction):
        logger.info(f"Setup risk calculator command invoked by {interaction.user.name}")
        content = (
            "> **📊 𝐂𝐘𝐏𝐇𝐄𝐑 𝐀𝐒𝐒𝐄𝐓𝐒 — 𝐑𝐈𝐒𝐊 𝐂𝐀𝐋𝐂𝐔𝐋𝐀𝐓𝐎𝐑**\n"
            "> \n"
            "> Within the **Cypher Assets Collective**, disciplined risk management is the bedrock of sustainable profitability.\n"
            "> \n"
            "> **How to Utilize:**\n"
            "> 1. Click the `📊 Calculate Position Size` button below.\n"
            "> 2. Enter your **Account Balance**, **Risk Percentage**, **Entry Price** and **Stop-Loss Price**.\n"
            "> 3. Receive your calculated lot size instantly.\n"
            "> \n"
            "> **Precision. Discipline. Profit.** 🏛️"
        )
        
        await interaction.channel.send(content=content, view=RiskCalculatorView())
        await interaction.response.send_message("✅ Risk Calculator panel posted.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Tools(bot))
