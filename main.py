# main.py - CYPHER-BOT V2 - Production Ready
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import logging
import sys
import traceback

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("CypherBot")

# --- Environment Variables (Validated at Startup) ---
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
APPLICATION_ID = os.getenv("APPLICATION_ID")

# Validate essential environment variables BEFORE anything else
missing = []
if not TOKEN:
    missing.append("DISCORD_TOKEN")
if not GUILD_ID:
    missing.append("GUILD_ID")
if not APPLICATION_ID:
    missing.append("APPLICATION_ID")

if missing:
    logger.critical(f"FATAL: Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

# Convert to int after validation (with error handling)
try:
    GUILD_ID_INT = int(GUILD_ID)
except ValueError:
    logger.critical(f"FATAL: GUILD_ID '{GUILD_ID}' is not a valid integer.")
    sys.exit(1)

try:
    APPLICATION_ID_INT = int(APPLICATION_ID)
except ValueError:
    logger.critical(f"FATAL: APPLICATION_ID '{APPLICATION_ID}' is not a valid integer.")
    sys.exit(1)

# Ensure GUILD_ID is available as a string env var for cogs
os.environ["GUILD_ID"] = str(GUILD_ID_INT)

# --- Flask Health Check Server ---
# Railway requires a web process or health check endpoint.
# We run Flask in a daemon thread so it doesn't block the bot.
def start_health_server():
    """Start a minimal Flask health check server for Railway."""
    try:
        from flask import Flask
        health_app = Flask(__name__)

        @health_app.route("/")
        def health():
            return "CYPHER-BOT is online.", 200

        port = int(os.environ.get("PORT", 8080))
        # Use threaded=True for handling concurrent health checks
        health_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.warning(f"Health check server failed to start: {e}")
        logger.warning("This is non-critical — the bot will continue running.")


# --- Discord Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# --- Explicit Cog List ---
# Only these cogs will be loaded. No dynamic scanning.
# Removed: orderflow_walls, liquidity_heatmap, alpha_intelligence (permanently deleted)
STABLE_COGS = [
    "crypto_news",
    "cypher_ai",
    "graduation",
    "inactivity",
    "mentorship",
    "moderation",
    "onboarding",
    "stats_engine",
    "tickets",
    "tools",
    "trading_terms",
    "verification",
    "welcome",
]


# --- Bot Definition ---
class CypherBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            application_id=APPLICATION_ID_INT,
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="Cypher Assets 🏛️"
            ),
        )
        self.synced = False

    async def setup_hook(self):
        """Runs before the bot connects to Discord."""
        logger.info("--- setup_hook started ---")

        # 1. Start Flask health check server in a daemon thread
        import threading

        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        logger.info("Health check server started on background thread.")

        # 2. Load cogs from explicit list
        logger.info(f"Loading {len(STABLE_COGS)} cogs...")
        loaded = 0
        failed = 0
        for cog_name in STABLE_COGS:
            extension = f"cogs.{cog_name}"
            try:
                await self.load_extension(extension)
                logger.info(f"  [OK] {cog_name}")
                loaded += 1
            except Exception as e:
                logger.error(f"  [FAIL] {cog_name}: {e}")
                traceback.print_exc()
                failed += 1

        logger.info(f"Cog loading complete: {loaded} loaded, {failed} failed.")
        logger.info("--- setup_hook complete ---")

    async def on_ready(self):
        """Fires when the bot is fully connected to Discord."""
        logger.info("=" * 60)
        logger.info("CYPHER-BOT V2 IS ONLINE")
        logger.info(f"  User:  {self.user} (ID: {self.user.id})")
        guild = self.get_guild(GUILD_ID_INT)
        if guild:
            logger.info(f"  Guild: {guild.name} (ID: {guild.id})")
        else:
            logger.warning(f"  Guild {GUILD_ID_INT} not found — bot may not be in the server.")
        logger.info("=" * 60)

        # Set presence
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="Cypher Assets 🏛️"
            ),
        )

        # Sync slash commands to guild (only once)
        if not self.synced:
            try:
                guild_obj = discord.Object(id=GUILD_ID_INT)
                synced_commands = await self.tree.sync(guild=guild_obj)
                self.synced = True
                logger.info(f"Synced {len(synced_commands)} slash commands to guild.")
            except Exception as e:
                logger.error(f"Failed to sync slash commands: {e}")
                traceback.print_exc()


# --- Main Execution ---
if __name__ == "__main__":
    bot = CypherBot()
    try:
        logger.info("Starting CYPHER-BOT V2...")
        bot.run(TOKEN, log_handler=None)  # log_handler=None prevents discord.py from overriding our logging
    except discord.LoginFailure:
        logger.critical("FATAL: Invalid DISCORD_TOKEN. Check your environment variables.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"FATAL: Unhandled exception: {e}")
        traceback.print_exc()
        sys.exit(1)
