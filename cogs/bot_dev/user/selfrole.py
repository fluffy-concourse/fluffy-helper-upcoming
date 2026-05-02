###############################################
#
# File: cogs.bot_dev.user.selfrole
# Date: 23/04/2026 (EU)
# Author: snow2code
#
###############################################


import re
import emoji

from discord.ext import commands
from utils.semibot import *
from utils.globals import Globals

def contains_emoji(text):
    return bool(emoji.emoji_count(text)) # Returns True if emojis are present

class BotDevCommands__User__SelfRole(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.guild_only()
    @commands.hybrid_command(name="selfroles")
    async def selfroles(self, ctx: Context):
        """
        Meow

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 1403877222959419423:
            pass
        else:
            await ctx.reply("That command is only usable by the bot developer.")
            return
        
        self_roles = Globals.selfroles
        embed = discord.Embed(title="Self Roles", description="")

        for role in self_roles:
            embed.description = f"{embed.description}\n{role['emoji']} - {role['role_id']} (<@&{role['role_id']}>)"
        
        await ctx.reply(embed=embed, silent=True)

    @commands.guild_only()
    @commands.hybrid_command(name="addselfrole")
    async def addselfrole(self, ctx: Context, emoji: str, roleself: discord.Role, channel: discord.TextChannel):
        """
        Meow

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        emoji: str
            The emoji for the self role
        role: discord.Role
            The role for the self role
        channel: discord.TextChannel
            The channel that it'll work for
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 1403877222959419423:
            pass
        else:
            await ctx.reply("That command is only usable by the bot developer.")
            return
        
        self_roles = Globals.selfroles
        already_self_role = False

        for role in self_roles:
            if role['role_id'] == roleself.id:
                already_self_role = True
                await ctx.reply(f"The role `{roleself.name}` is already a self role.")
            
            if role['emoji'] == emoji:
                already_self_role = True
                await ctx.reply(f"The emoji {emoji} is already used.")

        if already_self_role == False:
            try:
                conn = SemiData.selfroles_conn
                emoji_id = 0
                if contains_emoji(emoji) == False:
                    emoji = emoji.lower()
                    emoji_a = re.sub(r"[<_:a-z>]", "", emoji)
                    emoji_id = int(emoji_a)

                conn.execute(f"INSERT INTO reaction_roles (emoji, emoji_id, channel_id, role_id) VALUES (?, ?, ?, ?)", (f'{emoji}', int(emoji_id), channel.id, roleself.id))
                conn.commit()
                await ctx.reply(f"Successfully added `{roleself.name}` ({roleself.id}) to self roles.")
            except Exception as e:
                await ctx.reply(f"Failed to add self role.\n`{e}`")

        Globals.update_selfroles(self.bot.logger)
            
    @commands.guild_only()
    @commands.hybrid_command(name="removeselfrole")
    async def removeselfrole(self, ctx: Context, roleself: discord.Role):
        """
        Meow

        Parameters
        ----------
        ctx: Context
            The context of the command invokation
        role: discord.Role
            The role for the self role
        """
        if SemiBot.command_disabled(ctx):
            await ctx.reply("That command is currently disabled.")
            return
        
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 1403877222959419423:
            pass
        else:
            await ctx.reply("That command is only usable by the bot developer.")
            return
        
        self_roles = SemiData.selfroles_conn

        for role in Globals.selfroles:
            if role['role_id'] == roleself.id:
                try:
                    self_roles.cursor().execute(f'DELETE FROM reaction_roles WHERE role_id={roleself.id}')
                    self_roles.commit()

                    await ctx.reply(f"Successfully removed `{roleself.name}` ({roleself.id}) from self roles.")
                except Exception as e:
                    await ctx.reply(f"Failed to remove self role.\n`{e}`")

        Globals.update_selfroles(self.bot.logger)
            
async def setup(bot):
    await bot.add_cog(BotDevCommands__User__SelfRole(bot))
