##################################################
#
# File: cogs.user.misc.afk
# Date: 02/05/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##################################################

from discord.ext import commands
from utils.globals import Globals
from utils.semibot import *

class UserCommands__Misc__Afk(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    ## Values for database table:
    # 0 - user_id
    # 1 - nickname
    # 2 - message
    # 3 - afk_since
    # 4 - toggle

    @commands.guild_only()
    @commands.hybrid_command(name="afk")
    async def afk(self, ctx: Context, *, message: str = "Gone Fishin'", return_message: bool = True):
        """
        Set your status to AFK

        Parameters
        ----------
        ctx: Context
            The context of the command invocation
        message: str
            The message you want to use
        return_message: str
            Toggle the return message (UNUSED)
        """

        # if not isinstance(ctx.channel, discord.DMChannel):
        await SemiBot.log_command(self.bot, ctx.author, ctx)

        if Globals.is_user_afk(ctx.author.id) != False:
            await ctx.reply("Your status is already set to AFK.\n \
                -# Did you mean to update your AFK message? (?afkupdate message)\n \
                -# Did you mean to toggle your AFK status from being removed? (?afktoggle)\n \
            ")
            return
        
        # Now we know their status isn't AFK.. Let's set it
        user_nick = SemiBot.get_user_nick(ctx.author)
        nickname = user_nick['nick']
        afk_since = ctx.message.created_at.strftime("%d/%m/%Y %H:%M")

        afk_msg_base = f"I've set your status to AFK with the message `{message}`"

        SemiData.userdata_conn.execute(f'INSERT INTO afk_users VALUES ({ctx.author.id}, {ctx.guild.id}, "{nickname}", "{message}", "{afk_since}", 0)')
        SemiData.userdata_conn.commit()

        try:
            await ctx.author.edit(nick=f"[AFK] {nickname}")
            await ctx.reply(f"{afk_msg_base}")
        except discord.errors.HTTPException as e:
            # Nick character limit
            if e.text.find("In nick: Must be 32 or fewer in length."):
                await ctx.reply(f"{afk_msg_base}\n..however I cannot put 'AFK' in your nickname because of the nickname character limit. (32 max.)")
        except discord.errors.Forbidden as e:
            if e.text == "Missing Permissions":
                await ctx.reply(f"{afk_msg_base}\n..however I cannot change your nickname to show you're AFK.")

        Globals.update_afk(self.bot.logger, ctx.guild.id)
            
async def setup(bot):
    await bot.add_cog(UserCommands__Misc__Afk(bot))
