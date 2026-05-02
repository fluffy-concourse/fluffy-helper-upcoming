###############################################
#
# File: cogs.bot_dev.reload
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################


import os
import importlib

from discord.ext import commands
from utils.semibot import *

class BotDevCommands__Bot__Reload(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    ## events

    @commands.guild_only()
    @commands.hybrid_command(name="unloadlisteners")
    async def unloadlisteners(self, ctx: Context):
        """
        And now I'll wave, so long! -- Placeholder

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

        success = []
        failed = []
        
        listeners = 0
        for what in os.listdir("listeners"):
            gud = True
            if what == "__pycache__":
                gud = False
            else:
                if what.endswith(".py"):
                    gud = False
                    listeners = listeners + 1
                    name = what[:-3]
                    try:
                        await self.bot.unload_extension(f"listeners.{name}")
                        success.append(f"listeners.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{name} - {e}")

            if gud:
                for file in os.listdir(f"listeners/{what}"):
                    # Ignore files that aren't .py files
                    if not file.endswith(".py"):
                        continue

                    listeners = listeners + 1
                    name = file[:-3]
                    try:
                        await self.bot.unload_extension(f"listeners.{what}.{name}")
                        success.append(f"listeners.{what}.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{what}.{name} - {e}")
         
        successA = ""
        failedA = ""

        for a in success:
            successA = f"{successA}\n{a}"
        for a in failed:
            failedA = f"{failedA}\n{a}"
        with open("logs/reload_all_success.txt", "w") as f:
            f.write(successA)
        with open("logs/reload_all_failed.txt", "w") as f:
            f.write(failedA)

        await ctx.send(files=[discord.File("logs/reload_all_success.txt"), discord.File("logs/reload_all_failed.txt")])
        os.remove("logs/reload_all_success.txt")
        os.remove("logs/reload_all_failed.txt")
            
        try:
            await self.bot.unload_extension(f"listeners.{what}.{name}")
            await ctx.reply(f"Unloaded `listeners.{what}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="loadlisteners")
    async def loadlisteners(self, ctx: Context):
        """
        And now I'll wave, so long! -- Placeholder

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

        success = []
        failed = []
        
        listeners = 0
        for what in os.listdir("listeners"):
            gud = True
            if what == "__pycache__":
                gud = False
            else:
                if what.endswith(".py"):
                    gud = False
                    listeners = listeners + 1
                    name = what[:-3]
                    try:
                        await self.bot.load_extension(f"listeners.{name}")
                        success.append(f"listeners.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{name} - {e}")

            if gud:
                for file in os.listdir(f"listeners/{what}"):
                    # Ignore files that aren't .py files
                    if not file.endswith(".py"):
                        continue

                    listeners = listeners + 1
                    name = file[:-3]
                    try:
                        await self.bot.load_extension(f"listeners.{what}.{name}")
                        success.append(f"listeners.{what}.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{what}.{name} - {e}")
         
        successA = ""
        failedA = ""

        for a in success:
            successA = f"{successA}\n{a}"
        for a in failed:
            failedA = f"{failedA}\n{a}"
        with open("logs/reload_all_success.txt", "w") as f:
            f.write(successA)
        with open("logs/reload_all_failed.txt", "w") as f:
            f.write(failedA)

        await ctx.send(files=[discord.File("logs/reload_all_success.txt"), discord.File("logs/reload_all_failed.txt")])
        os.remove("logs/reload_all_success.txt")
        os.remove("logs/reload_all_failed.txt")
            
        try:
            await self.bot.unload_extension(f"listeners.{what}.{name}")
            await ctx.reply(f"Unloaded `listeners.{what}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")


    @commands.guild_only()
    @commands.hybrid_command(name="reloadlistener")
    async def reloadlistener(self, ctx: Context, what: str, name: str):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the listener is in (e.g audit_logs)
        name: str
            The file name of the listener (e.g message_deleted)
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
        
        try:
            await self.bot.reload_extension(f"listeners.{what}.{name}")
            await ctx.reply(f"Reloaded `listeners.{what}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="loadlistener")
    async def loadlistener(self, ctx: Context, what: str, name: str):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the listener is in (e.g audit_logs)
        name: str
            The file name of the listener (e.g message_deleted)
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
        
        try:
            await self.bot.load_extension(f"listeners.{what}.{name}")
            await ctx.reply(f"Loaded `listeners.{what}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="unloadlistener")
    async def unloadlistener(self, ctx: Context, what: str, name: str):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the listener is in (e.g audit_logs)
        name: str
            The file name of the listener (e.g message_deleted)
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
        
        try:
            await self.bot.unload_extension(f"listeners.{what}.{name}")
            await ctx.reply(f"Unloaded `listeners.{what}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    ## Commands
    @commands.guild_only()
    @commands.hybrid_command(name="reload")
    async def reload(self, ctx: Context, what: str, sub: str, name: str):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the command is in (e.g staff)
        sub: str
            The sub folder it's in (e.g silly)
        name: str
            The file name of the command (e.g cutinate)
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
        
        try:
            await self.bot.reload_extension(f"cogs.{what}.{sub}.{name}")
            await ctx.reply(f"Reloaded `cogs.{what}.{sub}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="load")
    async def load(self, ctx: Context, what: str, sub: str, name: str):
        """
        And now I'll wave, so long! -- Placeholder

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the command is in (e.g staff)
        sub: str
            The sub folder it's in (e.g silly)
        name: str
            The file name of the command (e.g cutinate)
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
        
        try:
            await self.bot.load_extension(f"cogs.{what}.{sub}.{name}")
            await ctx.reply(f"Loaded `cogs.{what}.{sub}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="unload")
    async def unload(self, ctx: Context, what: str, sub: str, name: str):
        """
        Unload a command.

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        what: str
            The category the command is in (e.g staff)
        sub: str
            The sub folder it's in (e.g silly)
        name: str
            The file name of the command (e.g cutinate)
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
        
        try:
            await self.bot.unload_extension(f"cogs.{what}.{sub}.{name}")
            await ctx.reply(f"Unloaded `cogs.{what}.{sub}.{name}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.guild_only()
    @commands.hybrid_command(name="reloadall")
    async def reloadall(self, ctx: Context):
        """
        Reload all listeners and commands.

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

        success = []
        failed = []
        
        listeners = 0
        commands = 0
        for what in os.listdir("listeners"):
            gud = True
            if what == "__pycache__":
                gud = False
            else:
                if what.endswith(".py"):
                    gud = False
                    listeners = listeners + 1
                    name = what[:-3]
                    try:
                        await self.bot.reload_extension(f"listeners.{name}")
                        success.append(f"listeners.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{name} - {e}")

            if gud:
                for file in os.listdir(f"listeners/{what}"):
                    # Ignore files that aren't .py files
                    if not file.endswith(".py"):
                        continue

                    listeners = listeners + 1
                    name = file[:-3]
                    try:
                        await self.bot.reload_extension(f"listeners.{what}.{name}")
                        success.append(f"listeners.{what}.{name}")
                    except Exception as e:
                        failed.append(f"listeners.{what}.{name} - {e}")
            
        ## Load command cogs
        for who in os.listdir("cogs"):
            gud = True
            if who == "__pycache__":
                gud = False

            if gud:
                for sub in os.listdir(f"cogs/{who}"):
                    if sub != "__pycache__":
                        if sub.endswith(".py"):
                            commands = commands + 1
                            name = sub[:-3]
                            try:
                                await self.bot.reload_extension(f"cogs.{who}.{name}")
                                success.append(f"cogs.{who}.{name}")
                            except Exception as e:
                                failed.append(f"cogs.{who}.{name} - {e}")
                        else:
                            for file in os.listdir(f"cogs/{who}/{sub}"):
                                # Ignore files that aren't .py files
                                if not file.endswith(".py"):
                                    continue
                                
                                commands = commands + 1
                                name = file[:-3]
                                try:
                                    await self.bot.reload_extension(f"cogs.{who}.{sub}.{name}")
                                    success.append(f"cogs.{who}.{sub}.{name}")
                                except Exception as e:
                                    failed.append(f"cogs.{who}.{sub}.{name} - {e}")


        successA = ""
        failedA = ""

        for a in success:
            successA = f"{successA}\n{a}"
        for a in failed:
            failedA = f"{failedA}\n{a}"
        with open("logs/reload_all_success.txt", "w") as f:
            f.write(successA)
        with open("logs/reload_all_failed.txt", "w") as f:
            f.write(failedA)

        await ctx.send(files=[discord.File("logs/reload_all_success.txt"), discord.File("logs/reload_all_failed.txt")])
        os.remove("logs/reload_all_success.txt")
        os.remove("logs/reload_all_failed.txt")
            
    @commands.hybrid_command(name="reloadutil")
    async def reloadutil(self, ctx: Context, name: str):
        """
        And now I'll wave, so long! -- Placeholder

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
        
        name_maker = f"utils/{name}.py"

        try:
            module_name = importlib.import_module(f"utils.{name}")
            await ctx.reply(f"Reloaded util module `{name}`")
        except ModuleNotFoundError:
            return await ctx.send(f"Couldn't find module named `{name_maker}`")
        except Exception as e:
            await ctx.reply(f"`{e}`")

    @commands.hybrid_command(name="reloadutils")
    async def reloadutils(self, ctx: Context):
        """
        MAnd now I'll wave, so long! -- Placeholder

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
        
        success = []
        failed = []
            
        for what in os.listdir("utils"):
            if what.endswith(".py"):
                name_maker = f"utils/{what}"
                try:
                    module_name = importlib.import_module(f"utils.{what[:-3]}")
                    success.append(f"utils.{what[:-3]}")
                # except ModuleNotFoundError:
                #     failed.append(f"utils.{what} - Couldn't find module named `{name_maker}`")
                except Exception as e:
                    failed.append(f"utils.{what} - {e}")

        successA = ""
        failedA = ""

        for a in success:
            successA = f"{successA}\n{a}"
        for a in failed:
            failedA = f"{failedA}\n{a}"
        with open("logs/reload_utils_success.txt", "w") as f:
            f.write(successA)
        with open("logs/reload_utils_failed.txt", "w") as f:
            f.write(failedA)

        await ctx.reply(
            files=[
                discord.File("logs/reload_utils_success.txt"),
                discord.File("logs/reload_utils_failed.txt")
            ]
        )
        os.remove("logs/reload_utils_success.txt")
        os.remove("logs/reload_utils_failed.txt")


async def setup(bot):
    await bot.add_cog(BotDevCommands__Bot__Reload(bot))
