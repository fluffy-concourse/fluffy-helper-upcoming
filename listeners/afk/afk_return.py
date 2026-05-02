##################################################
#
# File: listeners.afk.afk_return
# Date: 24/04/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##################################################


import discord

from datetime import datetime
from discord.ext import commands
from discord.errors import *
from discord.ext.commands.errors import *
from utils.globals import *
from utils.semibot import *
from utils.semidata import *

class AFKReturn(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if isinstance(msg.channel, discord.DMChannel):
            return
        
        afk_data = Globals.afk_users

        if not msg.content.startswith("?"):
            if Globals.is_user_afk(msg.author.id) != False:
                afk_entry = Globals.is_user_afk(msg.author.id)
                toggle = SemiData.userdata_conn.execute(f"SELECT toggle FROM afk_users WHERE user_id = ?", (msg.author.id,)).fetchone()[0]
                        
                # 23/03/2026 (EU) - Pixie (the owner) asked / suggested a afk toggle..
                ## Values
                # 1 - Don't remove
                # 0 - Remove

                if toggle != 1:
                    afk_time = datetime.strptime(afk_entry['since'], "%d/%m/%Y %H:%M")
                    now_time = datetime.now()
                    afk_dur = now_time - afk_time
                            
                    seconds = int(afk_dur.total_seconds())
                    days = seconds // 86400
                    hours = (seconds & 86400) // 3600
                    minutes = (seconds % 3600) // 60
                    # secondsB = seconds & 60

                    if minutes > 1:
                        hours_text = "hour"
                        minutes_text = "minute"
                        days_text = "day"
                                        
                        if minutes > 1 or minutes == 0:
                            minutes_text = "minutes"
                        if hours > 1 or hours == 0:
                            hours_text = "hours"
                        if days > 1 or days == 0:
                            days_text = "days"
                                
                        ## Remove from database
                        conn = SemiData.userdata_conn
                        conn.execute(f"DELETE FROM afk_users WHERE user_id = {afk_entry['user_id']}")
                        conn.commit()

                        Globals.update_afk(self.bot.logger, msg.guild.id)

                        ## Now return message
                        try:
                            returnMessage = f"Welcome back {msg.author.mention}, I removed your AFK status."

                            # await msg.channel.send(content=f"Welcome back {msg.author.mention}, I removed your AFK status.", delete_after=5)

                            if minutes > 0 and hours == 0 and days == 0:
                                returnMessage = f"{returnMessage}\nYou've been AFK for {minutes} {minutes_text}"
                            if hours > 0 and days == 0:
                                returnMessage = f"{returnMessage}\nYou've been AFK for {hours} {hours_text}, {minutes} {minutes_text}"
                            if days > 0:
                                returnMessage = f"{returnMessage}\nYou've been AFK for {days} {days_text}, {hours} {hours_text}, {minutes} {minutes_text}"
                                    
                            await msg.channel.send(content=f"{returnMessage}", delete_after=5)
                            await msg.author.edit(nick=afk_entry['name'], reason="They are back")
                        except Forbidden as e:
                            print(f"Cannot change {msg.author.display_name}'s name - {e}")
                            
async def setup(bot):
    await bot.add_cog(AFKReturn(bot))
