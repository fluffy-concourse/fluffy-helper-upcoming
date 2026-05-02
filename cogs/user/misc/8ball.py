##################################################
#
# File: cogs.user.misc.8ball
# Date: 02/05/2025
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##################################################


import random

# from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class UserCommands__Misc__EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="8ball", aliases=["magic8ball"])
    async def magic8ball(self, ctx: Context, *, question: str):
        """
        The magic 8ball.

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        question: str
            The question to ask the magic 8ball
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if not isinstance(ctx.channel, discord.DMChannel):
        await SemiBot.log_command(self.bot, ctx.author, ctx)

        response = random.choice(["Very likely", "Yes", "No", "Maybe", "Ask again later", "Definitely not", ])
        embed = self.bot.create_embed(
            title="🎱 Magic 8Ball",
            description=f"**Question**\n{question}\n\n**Response**\n{response}...",
            color=discord.Color.pink()
        )

        await ctx.reply(embed=embed)
            
async def setup(bot):
    await bot.add_cog(UserCommands__Misc__EightBall(bot))
