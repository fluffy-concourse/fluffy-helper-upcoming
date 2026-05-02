from discord import *
from discord.ext import commands
from utils.semibot import *
from utils.globals import Globals

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.member.bot == False:
            self_roles = Globals.selfroles
            
            for selfrole in self_roles:
                if payload.channel_id == selfrole['channel_id']:
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(selfrole['role_id'])
                    member = payload.member
            
                    if payload.emoji.is_custom_emoji():
                        if payload.emoji.id == selfrole['emoji_id']:
                            try:
                                await member.add_roles(role, reason="Self Roles")
                            except Exception as e:
                                await Bot.log_a_thing_2("listeners.selfroles.on_raw_reaction_add", member.name, guild.id, e)
                    else:
                        if selfrole['emoji'] == payload.emoji.name:
                            try:
                                await member.add_roles(role, reason="Self Roles")
                            except Exception as e:
                                await Bot.log_a_thing_2("listeners.selfroles.on_raw_reaction_add", member.name, guild.id, e)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if member.bot == False:
            self_roles = Globals.selfroles
            
            for selfrole in self_roles:
                if payload.channel_id == selfrole['channel_id']:
                    role = guild.get_role(selfrole['role_id'])
            
                    if payload.emoji.is_custom_emoji():
                        if payload.emoji.id == selfrole['emoji_id']:
                            try:
                                await member.remove_roles(role, reason="Self Roles")
                            except Exception as e:
                                await Bot.log_a_thing_2("listeners.selfroles.on_raw_reaction_remove", member.name, guild.id, e)
                    else:
                        if selfrole['emoji'] == payload.emoji.name:
                            try:
                                await member.remove_roles(role, reason="Self Roles")
                            except Exception as e:
                                await Bot.log_a_thing_2("listeners.selfroles.on_raw_reaction_remove", member.name, guild.id, e)

async def setup(bot):
    await bot.add_cog(SelfRoles(bot))
