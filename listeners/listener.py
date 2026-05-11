###############################################
#
# File: listeners.listener
# Date: 05/05/2026 (EU)
# Date Edited: 10/05/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Purpose: A example file for Fluffy Bot Base
#  
# Author: snow2code
#
###############################################


from discord.ext import commands
from utils.semibot import *
from utils.globals import Globals

class ListenerExampleNoDir(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    # Example!
    # Refer to "https://discordpy.readthedocs.io/en/stable/api.html?highlight=event#event-reference" for a full list of events
    async def on_ready(self):
        print("listeners.listener  on_ready called!")
        pass

async def setup(bot):
    await bot.add_cog(ListenerExampleNoDir(bot))
