###############################################
#
# File: cogs.bot_dev.misc.web_api
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################



from discord.ext import commands
from utils.semibot import *

# import web.app as app_module

class BotDevCommands__Misc__WebAPI(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.hybrid_command(name="reloadweb")
    async def reloadweb(self, ctx: Context):
        """
        Reload the web modules

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
#         if SemiBot.command_disabled(ctx):
#             await ctx.reply("That command is currently disabled.")
#             return
        
#         if await self.bot.member_can_use_command("bot_dev", ctx):
#             if ctx.author.id == 1403877222959419423:
#                 pass
#             else:
#                 await ctx.reply("That command is only usable by the bot developer.")
#                 return
            
#         app_module.reload_all()
#         if os.name.lower() == "nt":
#             os.system("clear")
#         elif os.name.lower() == "posix":
#             print("\033c")
#             print("clear")
#             os.system("clear")
#         else:
#             os.system("cls")
#         print(os.name)
#         msg = """
# ```JSON
# {
#     "reload_all": {
#         "status": "Reloaded."
#     }
#     "clear_console": {
#         "status": "Cleared output."
#     }
# }
# ```"""
#         await ctx.reply(msg)
        
    @commands.hybrid_command(name="clearconsole")
    async def clearconsole(self, ctx: Context):
        """
        Clear the terminal (Doesn't override logs)

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
        
        if os.name.lower() == "nt":
            os.system("clear")
        elif os.name.lower() == "posix":
            print("\033c")
            print("clear")
            os.system("clear")
        else:
            os.system("cls")
        print(os.name)
            
        await ctx.reply('```JSON\n{\n   "status": "Clear output."\n}```')
     
async def setup(bot):
    await bot.add_cog(BotDevCommands__Misc__WebAPI(bot))
