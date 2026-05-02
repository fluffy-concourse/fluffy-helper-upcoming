######################################################
#
# File: cogs.server_owner_n_bot_dev.config.features
# Date: 02/05/2025 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
######################################################


import os
import enum
import json

from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class Features(str, enum.Enum):
    command_used_log = "command_used_log"
    log_audits = "log_audits"
    join_message = "join_message"
    leave_message = "leave_message"

class EnabledDisabled(str, enum.Enum):
    enable = "enable"
    disable = "disable"

def insure_entries_exist(data: dict):
    keys = json.load( open("_config/_/server_data_keys.json") )
    new_data = data

    for key in keys:
        if key in data:
            pass
        else:
            new_data[key] = {}
    
    return new_data

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
        
        # if not isinstance(ctx.channel, discord.DMChannel):
        await SemiBot.log_command(self.bot, ctx.author, ctx)

        if ctx.interaction:
            value = False
            if str(enable_disable.value).lower() == "enabled":
                value = True


            if os.path.exists(f"_config/server/{ctx.guild.id}.json"):
                with open(f"_config/server/{ctx.guild.id}.json", "r+", encoding="utf-8") as output:
                    try:
                        data = json.load(output)
                        data = insure_entries_exist(data)
                        data['features'][feature.value] = value

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully {enable_disable.value}d {feature.value} for your server!")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
            else:
                with open(f"_config/server/{ctx.guild.id}.json", "w") as output:
                    try:
                        data = insure_entries_exist({})
                        data['features'][feature.value] = value

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully {enable_disable.value}d {feature.value} for your server!")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
                    
            
            pass
        else:
            await ctx.reply("Use this as a app command (/set_role_id)")
        
            
async def setup(bot):
    await bot.add_cog(ServerOwnerAndBotDev__Config__Features(bot))
