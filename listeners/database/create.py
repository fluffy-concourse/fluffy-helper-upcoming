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
from utils.globals import Globals
from utils.semidata import SemiData

class Database_Create(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        SemiData.init()

        Globals.update_banished(self.bot.logger)
        Globals.update_jobs(self.bot.logger)

        for guild in self.bot.guilds:
            Globals.update_afk(self.bot.logger, guild.id)
        
        # Globals.update_selfroles(self.bot.logger)

        for guild in self.bot.guilds:
            # Fuck my fluffy life.. getting members in on_connect didn't work, on_ready it is...
            for member in guild.members:
                if member.bot == False:
                    user = SemiData.userdata_conn.execute(f'SELECT * FROM user_data WHERE user_id={member.id} AND server_id={guild.id}')
                    if len(user.fetchall()) < 1:
                        SemiData.userdata_conn.execute(f'INSERT INTO user_data VALUES (0, {member.id}, {guild.id}, "{member.name}", "NULL", 0, 0, 0)')
            
            SemiData.userdata_conn.commit()


async def setup(bot):
    await bot.add_cog(Database_Create(bot))
