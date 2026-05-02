###############################################
#
# File: cogs.bot_dev.bot.sync
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################



from discord.ext import commands
from utils.semibot import *
from utils.semidata import SemiData
from utils.globals import Globals

async def sync_commands(self, ctx: Context):
    try:
        synced = await self.bot.tree.sync()
        await ctx.reply(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        self.bot.logger.error(msg=f"Error: {e}")

class BotDevCommands__Bot__Sync(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


    @commands.hybrid_command(name="syncjobs")
    async def syncjobs(self, ctx: Context):
        """
        Sync the job list from the database

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if await self.bot.member_can_use_command("bot_dev", ctx):
            if ctx.author.id == 1403877222959419423:
                pass
            else:
                await ctx.reply("That command is only usable by the bot developer.")
                return
        
        Globals.update_jobs(self.bot.logger)
        await ctx.reply(f"Updating the job list in the background. This won't be displayed besides from this message.")


    @commands.hybrid_command(name="sync")
    async def sync(self, ctx: Context):
        """
        Sync the bot's commands

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if await self.bot.member_can_use_command("bot_dev", ctx):
            if ctx.author.id == 1403877222959419423:
                pass
            else:
                await ctx.reply("That command is only usable by the bot developer.")
                return
        
        await sync_commands(self, ctx)

    @commands.hybrid_command(name="syncafkusers")
    async def syncafkusers(self, ctx: Context):
        """
        Sync AFK users from the database.

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if await self.bot.member_can_use_command("bot_dev", ctx):
            if ctx.author.id == 1403877222959419423:
                pass
            else:
                await ctx.reply("That command is only usable by the bot developer.")
                return
        
        Globals.update_afk(self.bot.logger, ctx.guild.id)
        await ctx.reply(f"Syncing AFK Users in the background. This won't be displayed besides from this message.")

    @commands.hybrid_command(name="syncbanishedlist")
    async def syncbanishedlist(self, ctx: Context):
        """
        Sync the banished list from the database

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if await self.bot.member_can_use_command("bot_dev", ctx):
            if ctx.author.id == 1403877222959419423:
                pass
            else:
                await ctx.reply("That command is only usable by the bot developer.")
                return
        
        Globals.update_banished(self.bot.logger)
        await ctx.reply(f"Updating the banished list in the background. This won't be displayed besides from this message.")

async def setup(bot):
    await bot.add_cog(BotDevCommands__Bot__Sync(bot))
