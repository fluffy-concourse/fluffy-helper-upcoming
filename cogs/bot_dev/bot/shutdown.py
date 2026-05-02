###############################################
#
# File: cogs.bot_dev.bot.shutdown
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################



from discord.ext import commands
from utils.semibot import *

class BotDevCommands__Bot__Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="shutdown")
    async def shutdown(self, ctx: Context):
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
            
        # Scrapped idea: Lethal Company Life Support Offline gif.. custom made / remade.
        await ctx.reply("Life support offline.")
        self.bot.close()
            
async def setup(bot):
    await bot.add_cog(BotDevCommands__Bot__Shutdown(bot))
