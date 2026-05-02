##################################################
#
# File: listeners.afk.afk_mention
# Date: 24/04/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##################################################


import discord

from datetime import datetime
from discord.ext import commands
from utils.semibot import *
from utils.globals import Globals

class AFKMention(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if not isinstance(msg.channel, discord.DMChannel):
            return
        
        if msg.author.bot:
            return
            
        if len(msg.mentions) > 0:
            for mention in msg.mentions:
                if Globals.is_user_afk(mention.id) != False:
                    afk_user = Globals.is_user_afk(mention.id)

                    afk_time = datetime.strptime(afk_user['since'], "%d/%m/%Y %H:%M")
                    now_time = datetime.now()
                    afk_dur = now_time - afk_time
                    seconds = int(afk_dur.total_seconds())
                        
                    days = seconds // 86400
                    hours = (seconds & 86400) // 3600
                    minutes = (seconds % 3600) // 60
                    # secondsB = seconds & 60

                    hours_text = "hour"
                    minutes_text = "minute"
                    days_text = "day"
                        
                    if minutes > 1 or minutes == 0:
                        minutes_text = "minutes"
                    if hours > 1 or hours == 0:
                        hours_text = "hours"
                    if days > 1 or days == 0:
                        days_text = "days"

                    if minutes > 0 and hours == 0 and days == 0:
                        await msg.reply(f"`{afk_user['name']}` is AFK: {afk_user['message']}\nThey've been AFK for {minutes} {minutes_text}")
                    if hours > 0 and days == 0:
                        await msg.reply(f"`{afk_user['name']}` is AFK: {afk_user['message']}\nThey've been AFK for {hours} {hours_text}, {minutes} {minutes_text}")
                    if days > 0:
                        await msg.reply(f"`{afk_user['name']}` is AFK: {afk_user['message']}\nThey've been AFK for {days} {days_text}, {hours} {hours_text}, {minutes} {minutes_text}")

                    break

async def setup(bot):
    await bot.add_cog(AFKMention(bot))