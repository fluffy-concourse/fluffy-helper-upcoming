###############################################
#
# File: listeners.database.
# Date: 10/05/2026 (EU)
# Date Edited: 
# Project: Fluffy Concourse - Fluffy Helper Bot
# Purpose: 
#  
# Author: snow2code
#
###############################################


from discord.ext import commands
from utils.semibot import Bot


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(msg=f"")
        self.bot.logger.info(msg=f"Logged in as {self.bot.user.name}")

        pass

async def setup(bot):
    await bot.add_cog(Ready(bot))