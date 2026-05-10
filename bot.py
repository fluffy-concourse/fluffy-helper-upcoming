###############################################
#
# File: bot
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################


import os
import discord
import dotenv
from utils.semibot import Bot
from utils.config import SemiConfig

good_to_go = True

if not os.path.exists(".env"):
    good_to_go = False
    
    print('''
    You need a ".env" file!
          
    Instructions:
    Rename ".env.example" to ".env"
    Replace "DISCORD_TOKEN" in the ".env" file with your bot's token.

    ''')


if good_to_go:
    # "Good to go!" - Robin Atkin Downes / TF2 Medic Voice Actor
    dotenv.load_dotenv()

    token = os.getenv('DISCORD_TOKEN')
    config = SemiConfig.get_config("main")

    bot = Bot(
        command_prefix=config['prefix'],
        prefix=config['prefix'], command_attrs=dict(hidden=True),
        allowed_mentions=discord.AllowedMentions(
            everyone=False, roles=True, users=True
        ),
        intents=discord.Intents.all(),
        help_command = None,
        case_insensitive=True
    )

    try:
        bot.run(token)
    except Exception as e:
        bot.logger.error(f"Error when logging in: {e}")
