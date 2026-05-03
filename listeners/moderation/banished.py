##################################################
#
# File: 
# Date: 21/03/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##################################################


import re

from utils.globals import Globals
from discord.ext import commands
from utils.semibot import discord, SemiBot, Bot

class UserCommands__Whatever__(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        pass
        # Ignore DMs
        # if isinstance(msg.channel, discord.DMChannel):
        #     return
        

        # banished = Globals.banished_words
        # banished_nodelete = Globals.banished_flagmsg
        # banished_words_noignore = Globals.banished_words_noignore
        # banished_ignore = Globals.banished_words_bypasses
        # # banished_words_private = banished_words_privateA.private_banished()

        # msg_content_lower = msg.content.lower()
        # content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower)
        # # content_lower_final = re.sub(r'[(#@-_\\/^,.)]', '', msg_content_lower).replace(" ", "")
        # canBanish = "Yes, banish it"
        
        # if msg.author.bot == False:
        #     shouldBanish = True

        #     for ignore in banished_ignore:
        #         if content_lower_final.find(ignore) >= 0:
        #             # self.bot.logger.info(msg=f"Don't banish '{msg_content_lower}' sent by {msg.author.name}")
        #             shouldBanish = False

        #     for thing in banished_nodelete:
        #         if content_lower_final.find(thing) >= 0:
        #             await SemiBot.moderate_user(self.bot, msg, msg.author, "message_banished_flagged", [None, thing])
        #             shouldBanish = False


        #     if await self.bot.member_can_use_command("staff", msg) == False:
                
        #         # 1 - If a user is mentioned, and their userid has "67" in it, ignore
        #         if len(msg.mentions) > 0:
        #             for mention in msg.mentions:
        #                 if str(mention.id).find("67") >= 0:
        #                     canBanish = "No, Don't banish it"
        #                     # self.bot.logger.info(msg=f"Don't banish '{msg_content_lower}' sent by {msg.author.name}")
                
        #         # 12/03/2026
        #         # Emojis can hve 67 in it..
        #         # same with channel ids
        #         if msg_content_lower.find("<:") >= 0:
        #             canBanish = "Maybe banish it?"

        #         if msg_content_lower.find("<#") >= 0:
        #             canBanish = "Maybe banish it?"

        #         # 2 - If in counting and the message has 67 in it, ignore
        #         if msg.channel.id == 1419042219842736299 and msg_content_lower.find("67") >= 0:
        #             self.bot.logger.info(msg="We need them to count ffs!")
        #             canBanish = "No, Don't banish it"


        #         if canBanish in ["Yes, banish it", "Maybe banish it?"]:
        #             for banished_thing in banished:
        #                 # 12/03/2026
        #                 # Emojis can have 67 in it...
        #                 # same with channel ids
        #                 if banished_thing == "67" and msg_content_lower.find("<:") >= 0:
        #                     shouldBanish = False
        #                 if banished_thing == "67" and msg_content_lower.find("<#") >= 0:
        #                     shouldBanish = False

        #                 # 3 - If banished_thing in banished_ignore, do not banish
                            
        #                 if shouldBanish:
        #                     if msg_content_lower.find(banished_thing) >= 0:
        #                         # await msg.reply(banished[banished_thing])
        #                         await SemiBot.moderate_user(self.bot, msg, msg.author, "message_banished", [banished[banished_thing], banished_thing])
        #                         await msg.delete()
                    
        #         # Last now - Private banish word list
        #         # for banished_thing in banished_words_private:
        #         #     if msg_content_lower.find(banished_thing) >= 0:
        #         #         # await msg.reply(banished_words_private[banished_thing])
        #         #         await SemiFunc.moderate_user(self.bot, msg, msg.author, "message_banished", [banished_words_private[banished_thing], banished_thing])
        #         #         await msg.delete()
            
        #     if shouldBanish:
        #         # These are banished for ALL, even staff.
        #         for banished_thing in banished_words_noignore:
        #             if content_lower_final.find(banished_thing) >= 0:
        #                 # await msg.reply(banished_words_noignore[banished_thing])
        #                 await SemiBot.moderate_user(self.bot, msg, msg.author, "message_banished", [banished_words_noignore[banished_thing], banished_thing])
        #                 await msg.delete()
                

                
        #     # Banish Snowy Paws
        #     if msg.author.id == 888072934114074624 or msg.author.id == 1257541858809217035 or msg.author.id == 1094359688541372457 or msg.author.id == 1403877222959419423:
        #         pawMsg = "You've been banished from using snowy's paws."
        #         if msg.author.id == 888072934114074624:
        #             pawMsg = "You've been banished from using your paws."

        #         # First snowy, and only snowy for now
        #         if msg_content_lower.find("<:snowypawbs:1468047084664918278>") >= 0:
        #             await msg.reply(pawMsg)
        #             await msg.delete()
        #         if len(msg.stickers):
        #             for sticker in msg.stickers:
        #                 if sticker.name == "Snowy Pawbs" or sticker.name == "Snowy Pawbs Real":
        #                     await msg.reply(pawMsg)
        #                     await msg.delete()

        
        
async def setup(bot):
    await bot.add_cog(UserCommands__Whatever__(bot))
