# main.py - MASTER VERSION
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from flask import Flask
from threading import Thread
import logging
import sys
import traceback

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Environment Variables ---
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
APPLICATION_ID = os.getenv("APPLICATION_ID")

# Validate essential environment variables
if not TOKEN:
    logger.critical("❌ FATAL ERROR: DISCORD_TOKEN not set!")
    sys.exit(1)
if not GUILD_ID:
    logger.critical("❌ FATAL ERROR: GUILD_ID not set!")
    sys.exit(1)
if not APPLICATION_ID:
    logger.critical("❌ FATAL ERROR: APPLICATION_ID not set!")
    sys.exit(1)

# Convert to int after validation
GUILD_ID = int(GUILD_ID)
APPLICATION_ID = int(APPLICATION_ID)

# Set GUILD_ID as an environment variable for cogs to access
os.environ["GUILD_ID"] = str(GUILD_ID)

# --- Discord Intents ---
# Request all default intents and explicitly enable privileged ones
intents = discord.Intents.default()
intents.message_content = True  # Required for message content access
intents.members = True          # Required for member-related events/properties
intents.presences = True        # Required for presence updates

# --- Flask Server for Health Checks ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Cypher Bot is Online!"

def run_flask_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False) # debug=False for production

# --- Bot Definition ---
class CypherBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            intents=intents, 
            application_id=APPLICATION_ID,
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name="Cypher Assets 🏛️")
        )
        self.synced = False

    async def setup_hook(self):
        """Setup hook - runs before bot connects."""
        logger.info("🔧 Starting setup_hook...")
        
        # 1. Start Flask server for Railway health checks
        try:
            Thread(target=run_flask_server, daemon=True).start()
            logger.info("✅ Flask server task created and started in a new thread.")
        except Exception as e:
            logger.error(f"❌ Flask server setup failed: {e}")

        # 2. Load cogs (ONLY STABLE AND NECESSARY ONES)
        logger.info("📂 Loading stable cogs...")
        
        # Explicit list of stable cogs to load


        stable_cogs = [
            "moderation",
            "graduation",
            "tickets",
            "onboarding",
            "mentorship",
            "verification",
            "tools",
            "inactivity",
            "cypher_ai",
            "crypto_news",
            "stats_engine",
            "trading_terms",
            "welcome"
        ]
        
        cogs_loaded = 0
        for cog in stable_cogs:
            try:
                await self.load_extension(f"cogs.{cog}")
                logger.info(f"✅ Cog loaded: {cog}")
                cogs_loaded += 1
            except Exception as e:
                logger.error(f"❌ Failed to load cog {cog}: {e}")
                traceback.print_exc() # Print full traceback for cog loading errors
        
        logger.info(f"📂 Loaded {cogs_loaded} stable cogs.")
        logger.info("✅ setup_hook complete!")

    async def on_ready(self):
        logger.info(f"\n{'='*60}")
        logger.info(f"🏛️ CYPHER BOT IS ONLINE")
        logger.info(f"{'='*60}")
        logger.info(f"User: {self.user} (ID: {self.user.id})")
        logger.info(f"Guild: {GUILD_ID}")
        logger.info(f"{'='*60}\n")
        logger.info("✅ Bot successfully connected to Discord!") # NEW DEBUG LOG
        
        await self.change_presence(
            status=discord.Status.online, 
            activity=discord.Activity(type=discord.ActivityType.watching, name="Cypher Assets 🏛️")
        )
        logger.info("✅ Bot status forced to ONLINE")

        if not self.synced:
            try:
                await self.tree.sync(guild=discord.Object(id=GUILD_ID))
                self.synced = True
                logger.info("✅ Slash commands synced to guild.")
            except Exception as e:
                logger.error(f"❌ Failed to sync slash commands: {e}")
                traceback.print_exc()

    # ═════════════════════════════════════════════════════════════
    # ADMIN PERMISSION LOCK - This forces Discord to keep admin intent
    # ═════════════════════════════════════════════════════════════
    @app_commands.command(name="admin_check", description="[INTERNAL] Admin permission lock")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    @app_commands.default_permissions(administrator=True)
    async def admin_check(self, interaction: discord.Interaction):
        """Hidden command to lock admin permissions in Discord."""
        await interaction.response.send_message("✅ Admin permissions locked.", ephemeral=True)

# --- Main Execution Block ---
if __name__ == "__main__":
    bot = CypherBot()
    try:
        logger.info("🚀 Starting bot...")
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"❌ FATAL ERROR during bot runtime: {e}")
        traceback.print_exc()
