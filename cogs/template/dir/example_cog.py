###############################################
#
# File: cogs.template.dir.example_cog
# Date: 04/05/2026 (EU)
# Date Edited: 10/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import discord

from discord.ext import commands
from utils.semibot import Bot, SemiBot, Context

class ExampleCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="example")
    async def genboostmsg(self, ctx: Context):
    # If you want paramters:
    # async def genboostmsg(self, ctx: Context, *, example: str):
        """
        Example command

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        example: str
            Example
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
            
        # If you want the command to be usable by staff, the bot dev or whoever else
        # if not self.bot.member_can_use_command("bot_dev", ctx):
        #     await ctx.reply("That command is only usable by the bot developer")
        #     return
        
        await ctx.reply("Command ransuccessfully!")
        
async def setup(bot):
    await bot.add_cog(ExampleCommandCog(bot))

