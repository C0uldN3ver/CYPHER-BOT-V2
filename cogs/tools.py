# cogs/tools.py - CYPHER-BOT V2 (Risk Calculator)
import discord
from discord import app_commands, ui
from discord.ext import commands
import os
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

GUILD_ID = int(os.getenv("GUILD_ID", "0"))
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


class RiskCalculatorModal(ui.Modal, title="CYPHER ASSET \u2014 RISK CALCULATOR"):
    balance = ui.TextInput(
        label="Account Balance ($)",
        placeholder="e.g. 100000",
        min_length=1,
        max_length=15,
        required=True,
    )
    risk_pct = ui.TextInput(
        label="Risk Percentage (%)",
        placeholder="e.g. 0.5 or 1",
        min_length=1,
        max_length=5,
        required=True,
    )
    entry_price = ui.TextInput(
        label="Entry Price",
        placeholder="e.g. 1.08500",
        min_length=1,
        max_length=15,
        required=True,
    )
    sl_price = ui.TextInput(
        label="Stop-Loss Price",
        placeholder="e.g. 1.08350",
        min_length=1,
        max_length=15,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
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

            is_jpy = entry > 50 or sl_val > 50
            pip_multiplier = 100 if is_jpy else 10000
            pip_distance = abs(entry - sl_val) * pip_multiplier

            if pip_distance <= 0:
                raise ValueError("Entry Price and Stop-Loss Price cannot be the same.")

            risk_amount = bal * (risk / 100)
            lot_size = risk_amount / (pip_distance * 10)

            embed = discord.Embed(
                title="CYPHER ASSETS \u2014 RISK CALCULATOR",
                color=0xFFD700,
                timestamp=datetime.now(timezone.utc),
            )
            embed.add_field(
                name="ACCOUNT PARAMETERS:",
                value=(
                    f"> Balance: **${bal:,.2f}**\n"
                    f"> Risk Percentage: **{risk:.2f}%**\n"
                    f"> Entry Price: **{entry:.5f}**\n"
                    f"> Stop-Loss Price: **{sl_val:.5f}**"
                ),
                inline=False,
            )
            embed.add_field(
                name="EXECUTION DETAILS:",
                value=(
                    f"> **Pip Distance:** **{pip_distance:.1f} Pips**\n"
                    f"> **Amount at Risk:** **${risk_amount:,.2f}**\n"
                    f"> **Recommended Lot Size:** **{lot_size:.2f} Lots**"
                ),
                inline=False,
            )
            embed.add_field(
                name="\u200b",
                value=(
                    "> *Capital protection is the first step to profitability. "
                    "Ensure your entry aligns with the Cypher Protocol before execution. "
                    "Never over-leverage based on emotion.*"
                ),
                inline=False,
            )
            embed.set_footer(text="Cypher Assets Collective")
            await interaction.followup.send(embed=embed, ephemeral=True)

        except ValueError as e:
            logger.error(f"Risk Calculator Input Error: {e}")
            await interaction.followup.send(
                f"\u274c **Invalid Input.** {str(e)} Please ensure you enter valid numeric values.",
                ephemeral=True,
            )
        except Exception as e:
            logger.error(f"Unexpected error in Risk Calculator: {e}")
            await interaction.followup.send(
                "\u274c An unexpected error occurred. Please try again later.",
                ephemeral=True,
            )


class RiskCalculatorView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Calculate Position Size",
        style=discord.ButtonStyle.primary,
        emoji="\U0001f4ca",
        custom_id="calculate_risk_button",
    )
    async def calculate_risk(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(RiskCalculatorModal())


class Tools(commands.Cog):
    """Trading tools including the Risk Calculator."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.add_view(RiskCalculatorView())
        logger.info("Tools cog initialized. Persistent RiskCalculatorView registered.")

    @app_commands.command(
        name="setup_risk_calculator",
        description="[ADMIN] Post the Risk Calculator panel. (Owner only)",
    )
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    @is_owner_check()
    async def setup_risk_calculator(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        logger.info(f"Risk calculator setup by {interaction.user.name}")
        content = (
            "> **CYPHER ASSETS \u2014 RISK CALCULATOR**\n"
            "> \n"
            "> Within the **Cypher Assets Collective**, disciplined risk management "
            "is the bedrock of sustainable profitability.\n"
            "> \n"
            "> **How to Utilize:**\n"
            "> 1. Click the `Calculate Position Size` button below.\n"
            "> 2. Enter your **Account Balance**, **Risk Percentage**, "
            "**Entry Price** and **Stop-Loss Price**.\n"
            "> 3. Receive your calculated lot size instantly.\n"
            "> \n"
            "> **Precision. Discipline. Profit.**"
        )
        await interaction.channel.send(content=content, view=RiskCalculatorView())
        await interaction.followup.send("\u2705 Risk Calculator panel posted.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tools(bot))
