######################################################
#
# File: cogs.server_owner_n_bot_dev.config.features
# Date: 02/05/2025 (EU)
# Date Edited: 10/05/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Purpose:
#  
# Author: snow2code
#
######################################################


import enum

from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class Features(str, enum.Enum):
    dm_owner_errors = "dm_owner_errors"
    hug_boop_messages = "hug_boop_messages"
    command_used_log = "command_used_log"
    log_audits = "log_audits"
    join_message = "join_message"
    leave_message = "leave_message"


class EnabledDisabled(str, enum.Enum):
    enable = "enable"
    disable = "disable"

class ServerOwnerAndBotDev__Config__Features(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="set_feature")
    async def set_feature(self, ctx: Context, feature: Features = None, enable_disable: EnabledDisabled = None):
        """
        Enable or disable a feature.. Server owner only

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        feature: Features
            The role to set a ID for
        enable_disable: EnabledDisabled
            Enable or disable
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if ctx.author.id != ctx.guild.owner_id or \
            await self.bot.member_can_use_command("bot_dev", ctx) == False:

            await ctx.reply("Only the bot developer and server owner can use that command")
            return
        
        # # if not isinstance(ctx.channel, discord.DMChannel):
        await SemiBot.log_command(self.bot, ctx.author, ctx)

        if ctx.interaction:
            if feature != None and enable_disable != None:
                value = 0
                if str(enable_disable.value).lower() == "enabled":
                    value = 1
                try:
                    SemiData.server_config_conn.execute(f'UPDATE features SET value = ? WHERE feature_name = ? AND server_id = ?', (value, feature.value, ctx.guild.id))
                    SemiData.server_config_conn.commit()
                    await ctx.reply(f"Successfully {enable_disable.value}d {feature.value} for your server!")
                except Exception as e:
                    await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
            else:
                await ctx.reply("Check your paramters.\nEnable usage: /set_feature whatever enable\nDisable usage: /set_feature whatever disable")
        else:
            await ctx.reply("Use this as a app command (/set_role_id)")

async def setup(bot):
    await bot.add_cog(ServerOwnerAndBotDev__Config__Features(bot))
