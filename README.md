# Cypher Bot - Master Version

This is the clean, refactored version of the Cypher Bot, rebuilt from the ground up with all identified issues fixed and optimized for stability and performance.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd CYPHER-BOT-V2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_guild_id_here
APPLICATION_ID=your_application_id_here
OWNER_ROLE_ID=your_owner_role_id_here
PORT=8080
```

4. Run the bot:
```bash
python main.py
```

## Features

- **Moderation:** Kick and ban members
- **Verification:** Member verification system
- **Tickets:** Support ticket system
- **Onboarding:** New member onboarding
- **Mentorship:** Mentorship program
- **Graduation:** Member graduation system
- **Tools:** Risk calculator for traders
- **Crypto News:** Cryptocurrency news updates
- **Stats Engine:** Statistics tracking
- **Trading Terms:** Trading terminology glossary
- **Cypher AI:** AI-powered assistant
- **Inactivity:** Inactivity management
- **Welcome:** Welcome messages for new members

## Architecture

- **main.py:** Bot entry point and initialization
- **cogs/:** Individual feature modules
- **data/:** Data storage (JSON files)
- **requirements.txt:** Python dependencies
- **Procfile:** Railway deployment configuration

## Deployment

This bot is designed to run on Railway. Ensure all environment variables are set in the Railway dashboard.

## Support

For issues or questions, please refer to the master documentation or contact the development team.
