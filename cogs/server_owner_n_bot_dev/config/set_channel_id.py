############################################################
#
# File: cogs.server_owner_n_bot_dev.config.set_channel_id
# Date: 02/05/2025 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Author: snow2code
#
############################################################


import os
import enum
import json

from utils.globals import Globals
from discord.ext import commands
from utils.semibot import *

class Channels(str, enum.Enum):
    bot_logs = "bot_logs"
    verify = "verify"
    welcome = "welcome"
    self_roles = "self_roles"
    boosts = "boosts"
    general_chat = "general_chat"
    bot_commands = "bot_commands"
    audit = "audit"

def insure_entries_exist(data: dict):
    keys = json.load( open("_config/_/server_data_keys.json") )
    new_data = data

    for key in keys:
        if key in data:
            pass
        else:
            new_data[key] = {}
    
    return new_data

class ServerOwnerAndBotDev__Config__SetChannelId(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="set_channel_id")
    async def set_channel_id(self, ctx: Context, channel_name: Channels = None, use_channel: discord.TextChannel = None):
        """
        Set a channel id.. Server owner only

        Parameters
        ----------
        ctx: Union[Context, commands.context.Context]
            The context of the command invocation
        channel_name: Channels
            The channel to set a ID for
        use_channel: discord.Role
            The channel to use the ID of
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
                        data['channel_ids'][channel_name.value] = use_channel.id

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully set {channel_name.value} in the server config with {use_channel.mention}'s ID")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
            else:
                with open(f"_config/server/{ctx.guild.id}.json", "w") as output:
                    try:
                        data = insure_entries_exist({})
                        data['channel_ids'][channel_name.value] = use_channel.id

                        output.seek(0)
                        json.dump(data, output, indent=4)
                        # output.truncate()
                        await ctx.reply(f"Successfully set {channel_name.value} in the server config with {use_channel.mention}'s ID")
                    except Exception as e:
                        await ctx.reply(f"Unable to edit your server config for the bot.\nError: {e}")
                        # json.dump(data_prev, output, indent=4)
                    
            pass
        else:
            await ctx.reply("Use this as a app command (/set_channel_id)")
        
            
async def setup(bot):
    await bot.add_cog(ServerOwnerAndBotDev__Config__SetChannelId(bot))
