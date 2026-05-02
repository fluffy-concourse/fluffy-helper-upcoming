##########################################################
#
# File: cogs.server_owner_n_bot_dev.config.set_role_id
# Date: 02/05/2025 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
##########################################################


import os
import enum
import json

from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class Roles(str, enum.Enum):
    vanity_seperator = "vanity_seperator"
    cute = "cute"
    # shortie = "shortie"
    smol = "smol"
    explode = "explode"
    tall = "tall"
    silly = "silly"
    welcome_ping = "welcome_ping"
    verified = "verified"
    banished = "banished"

def insure_entries_exist(data: dict):
    keys = json.load( open("_config/_/server_data_keys.json") )
    new_data = data

    for key in keys:
        if key in data:
            pass
        else:
            new_data[key] = {}
    
    return new_data

class ServerOwnerAndBotDev__Config__SetRoleId(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="set_role_id")
    async def set_role_id(self, ctx: Context, role_name: Roles = None, use_role: discord.Role = None):
        """
        Set a role id.. Server owner only

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        role_name: Role
            The role to set a ID for
        use_role: discord.Role
            The role to use the ID of
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        # if not isinstance(ctx.channel, discord.DMChannel):
        await SemiBot.log_command(self.bot, ctx.author, ctx)

        if ctx.interaction:
            if os.path.exists(f"_config/server/{ctx.guild.id}.json"):
                with open(f"_config/server/{ctx.guild.id}.json", "r+", encoding="utf-8") as output:
                    try:
                        data = json.load(output)
                        data = insure_entries_exist(data)
                        data['role_ids'][role_name.value] = use_role.id

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully set {role_name.value} in the server config with {use_role.mention}'s ID")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
            else:
                with open(f"_config/server/{ctx.guild.id}.json", "w") as output:
                    try:
                        data = insure_entries_exist({})
                        data['role_ids'][role_name.value] = use_role.id

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully set {role_name.value} in the server config with {use_role.mention}'s ID")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
                    
            
            pass
        else:
            await ctx.reply("Use this as a app command (/set_role_id)")
        
            
async def setup(bot):
    await bot.add_cog(ServerOwnerAndBotDev__Config__SetRoleId(bot))
