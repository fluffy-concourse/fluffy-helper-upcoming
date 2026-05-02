from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class UserCommands__Radar__Sillydar(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="sillydar")
    async def sillydar(self, ctx: Context, user: discord.Member):
        """
        See how silly someone is!

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        user: user: Union[discord.Member, discord.User]
            The user to use the radar on
        """
        if user.bot:
            await ctx.reply("The radar command can't be used on bots")
            return
        
        if not isinstance(ctx.channel, discord.DMChannel):
            await SemiBot.log_command(self.bot, ctx.author, ctx)
        
        embed = await Globals.fluffyRadar(self.bot, ctx, user, "silly")
        await ctx.reply(embed=embed)
            
async def setup(bot):
    await bot.add_cog(UserCommands__Radar__Sillydar(bot))
