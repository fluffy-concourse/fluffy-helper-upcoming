###############################################
#
# File: utils.semibot
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################


import os
import discord
import logging
import logging.handlers

from typing import Union
from utils.config import SemiConfig
from utils.semidata import SemiData
# from utils.globals import Globals
from discord.ext import commands
from discord.ext.commands import AutoShardedBot

from datetime import datetime, timezone

class Context(commands.Context):
    """
    This class is used to overwrite discord.py's Context class.
    You can add your own methods here.
    Any functions you add will automatically become usable in ALL commands.
    """
    def __init__(self, **kwargs):
        # self.bot: "Bot"
        super().__init__(**kwargs)


class Bot(AutoShardedBot):
    def __init__(self, prefix: str = "!", *args, **kargs):
        super().__init__(*args, **kargs)

        # Directory "logs" doesn't exist? Create it!
        if not os.path.exists("logs"):
            os.mkdir("logs")
        
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)

        handler = logging.handlers.RotatingFileHandler(
            filename=f"./logs/{datetime.now().strftime('%d-%m-%Y %H-%M')}.log",
            encoding='utf-8',
            # maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger
        self.shutting_down = False
        # self.get_all_emojis() = self.emojis


    async def close(self):
        if self.is_ready():
            self.shutting_down = True
            await super().close()
        
    async def setup_hook(self):
        listeners = 0
        commands = 0

        ## Load listener cogs
        if os.path.exists("listeners"):
            for what in os.listdir("listeners"):
                gud = True
                if what == "__pycache__":
                    gud = False
                else:
                    if what.endswith(".py"):
                        gud = False
                        listeners = listeners + 1
                        name = what[:-3]
                        await self.load_extension(f"listeners.{name}")

                if gud:
                    for file in os.listdir(f"listeners/{what}"):
                        # Ignore files that aren't .py files
                        if not file.endswith(".py"):
                            continue

                        listeners = listeners + 1
                        name = file[:-3]
                        await self.load_extension(f"listeners.{what}.{name}")
            
        ## Load command cogs
        if os.path.exists("cogs"):
            for who in os.listdir("cogs"):
                gud = True
                if who == "__pycache__":
                    gud = False

                if gud:
                    for sub in os.listdir(f"cogs/{who}"):
                        if sub != "__pycache__":
                            if sub.endswith(".py"):
                                commands = commands + 1
                                name = sub[:-3]
                                await self.load_extension(f"cogs.{who}.{name}")
                            else:
                                for file in os.listdir(f"cogs/{who}/{sub}"):
                                    # Ignore files that aren't .py files
                                    if not file.endswith(".py"):
                                        continue
                                    
                                    commands = commands + 1
                                    name = file[:-3]
                                    await self.load_extension(f"cogs.{who}.{sub}.{name}")
            
        print(f"Loaded {commands} command files.\nLoaded {listeners} listener files.")
    
    # async def process_commands(self, msg: discord.Message):
    #     ctx = await self.get_context(msg, cls=Context)
    #     a = SemiConfig.get_config_wild("commands")
        
    #     if msg.content.lower().find("&topic") == 0:
    #         with open(files.get_filepath("commands", "json"), "r", encoding="utf8") as file:
    #             data = json.load(file)
    #             topics = data['topics']
                
    #             topic = random.choice(topics)

    #             await ctx.send(f"{topic}?")
    #     else:
    #         await self.invoke(ctx)



    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: commands.CommandError):
        err_handled = False

        if isinstance(error, commands.NoPrivateMessage):
            err_handled = True
            await ctx.reply("That command is only usable in a server.")
        elif isinstance(error, commands.BadArgument):
            err_handled = True
            await ctx.reply("A argument for that command is invalid... give it another try")
        elif isinstance(error, commands.MissingRequiredArgument):
            err_handled = True
            await ctx.reply("You *might* be missing a argument for that command... or something has gone terribly, *TERRIBLY* wrong.")
        elif isinstance(error, commands.CommandNotFound):
            err_handled = True
            return


        if not os.path.exists("logs/errors"):
            os.makedirs("logs/errors")


        command_name = ctx.command.name
        date = datetime.now().strftime('%d-%m-%Y at %H-%M-%S')

        if command_name == "mute":
            await ctx.reply(f"Argument missing or invaild duration. Duration Examples:\n5s-5 seconds\n5m-5 minutes\n5h-5 hours\n5d- 5 days\n\nMax duration is 28 days.")
            
        if err_handled == False:
            if SemiBot.server_configured(ctx):
                await Bot.log_a_thing(self, "utils.semibot", ctx.command.name, ctx.author.name, ctx.guild.id, error)
            await ctx.reply("An error occured with the command.")
            
    async def log_a_thing(self, file: str, command_name: str, author_name: str, guild_id: int, error):
        embed = SemiBot.error_embed(file, "error", f"{error}")
        
        guild = self.get_guild(guild_id)
        logs_id = await SemiBot.get_channel_id(guild, "bot_logs")
        logs = guild.get_channel(logs_id)

        date = datetime.now().strftime('%d-%m-%Y at %H-%M-%S')
        
        with open(f"logs/errors/{date}", "w") as f:
            f.write(f"An error occured with {command_name} ran by {author_name} on {date}\n\nError: {error}")
            
        self.logger.warn(f"An error occured with {command_name} ran by {author_name} on {date} - {error}")
        # await ctx.reply("An error occured with the command.")
        await logs.send(embed=embed)

    async def log_a_thing_2(self, file: str, author_name: str, guild_id: int, error):
        embed = SemiBot.error_embed(file, "error", f"{error}")
        
        guild = self.get_guild(guild_id)
        logs_id = await SemiBot.get_channel_id(guild, "bot_logs")
        logs = guild.get_channel(logs_id)

        date = datetime.now().strftime('%d-%m-%Y at %H-%M-%S')
        
        with open(f"logs/errors/{date}", "w") as f:
            f.write(f"An error occured in {file} (triggered by {author_name}) on {date}\n\nError: {error}")
            
        self.logger.warn(f"An error occured in {file} (triggered by {author_name}) on {date} - {error}")
        await logs.send(embed=embed)

    async def on_connect(self):
        # await self.bot.change_presence(status=discord.Status.invisible)

        try:
            synced = await self.tree.sync()
            self.logger.info(msg=f"Synced {len(synced)} commands globally.")
        except Exception as e:
            self.logger.error(msg=f"Error: {e}")

    # def create_embed_notitle(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: [] = []):
    def create_embed_notitle(self, description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: list = [], use_by_snow2code_footer: bool = False):
        embed = discord.Embed(description=description, color=color)
        
        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        if use_by_snow2code_footer:
            embed.set_footer(text="Bot developed by snow2code")

        return embed
    
    def create_embed(self, title:str = "Embed Title", description: str = "Embed Description", color: discord.Color = discord.Color.dark_embed(), fields: list = [], use_by_snow2code_footer: bool = False):
        embed = discord.Embed(title=title, description=description, color=color)
        
        if len(fields) > 0:
            for field in fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])

        if use_by_snow2code_footer:
            embed.set_footer(text="Bot developed by snow2code")
        
        return embed

    async def member_can_use_command(self, command_type: str, ctx: Context):
        command_type = command_type.lower()
        config = SemiConfig.get_config("role_ids")
        member: discord.Member = ctx.author
        
        if command_type == "bot_dev":
            if member.id == self.owner_id:
                return True
        elif command_type == "test":
            if member.id in config['testers']:
                return True
        elif command_type == "owner":
            if member.id in config['owners']:
                return True
        elif command_type == "staff":
            role = await SemiBot.get_role_id(ctx, "staff")

            if member.get_role(role):
                return True
        elif command_type == "user":
            return True
        return False
    

class SemiBot():
    def error_embed(file: str, give_type: str, message: str):
        type = ""
        color = discord.Color.dark_embed()
        if str.lower(give_type) in ["warn", "warning", "error"]:
            type = give_type.capitalize()
            if str.lower(give_type) in ["warn", "warning"]:
                color = discord.Color.yellow()
            elif str.lower(give_type) == "error":
                color = discord.Color.red()

        return discord.Embed( title=f'{file} - {type}', description=message, color=color, timestamp=datetime.now(timezone.utc) )

    async def moderate_user(bot: Bot, ctx: Context, user: discord.Member, moderation_type: str, args: list):
        moderation_embed = bot.create_embed_notitle()
        audit = ctx.guild.get_channel(await SemiBot.get_channel_id(ctx, "audit"))
        isGud = False

        
        if moderation_type == "banish":
            isGud = True
            moderation_embed.title = f"Staff at {ctx.guild.name}"
            moderation_embed.description = f"You've been banished in {ctx.guild.name} by {ctx.author.display_name}"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}"
            
            bot.logger.info(f"{ctx.author.name} banished {user.name}. Reason: {args[0]}")
        elif moderation_type == "kick":
            isGud = True
            moderation_embed.title = f"Staff at {ctx.guild.name}"
            moderation_embed.description = f"You've been kicked from {ctx.guild.name} by {ctx.author.display_name}"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}\n\n\nServer Invite: https://discord.gg/X8QqpeYgGF"
            
            bot.logger.info(f"{ctx.author.name} kicked {user.name}. Reason: {args[0]}")
        elif moderation_type == "ban":
            isGud = True
            moderation_embed.title = f"Staff at {ctx.guild.name}"
            moderation_embed.description = f"You've been banned from {ctx.guild.name} permanently by {ctx.author.display_name}"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}\n\n\nServer Invite: https://discord.gg/X8QqpeYgGF"
            
            bot.logger.info(f"{ctx.author.name} banned {user.name}. Reason: {args[0]}")
        elif moderation_type == "mute":
            isGud = True
            moderation_embed.title = f"Staff at {ctx.guild.name}"
            moderation_embed.description = f"You've been muted in {ctx.guild.name} by {ctx.author.display_name}"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}"
            
            bot.logger.info(f"{ctx.author.name} muted {user.name}. Reason: {args[0]}")
        elif moderation_type == "unmute":
            isGud = True
            moderation_embed.title = f"Staff at {ctx.guild.name}"
            moderation_embed.description = f"You've been unmuted in {ctx.guild.name} by {ctx.author.display_name}"
            moderation_embed.description = moderation_embed.description + f"\n\nReason: {args[0]}\nPunisher: {ctx.author.name}"

            bot.logger.info(f"{ctx.author.name} unmuted {user.name}. Reason: {args[0]}")
        elif moderation_type == "message_banished_flagged":
            # isGud = True
            moderation_embed.description = f"**Message sent by {ctx.author.mention} in {ctx.channel.mention} was flagged**"
            moderation_embed.description = moderation_embed.description + f"\n\nMessage: {ctx.content}\n"
            moderation_embed.description = moderation_embed.description + f"Detected flagged word: {args[1]}\n"
            moderation_embed.color = discord.Color.red()

            moderation_embed.timestamp = datetime.utcnow()
            moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            moderation_embed.set_footer(text=f"Author: {user.id} | Message ID: {ctx.id}")
            
            # await ctx.reply(f"{args[0]}")
            await audit.send(embed=moderation_embed)

            return
        elif moderation_type == "message_banished":
            # isGud = True
            moderation_embed.description = f"**Message sent by {ctx.author.mention} in {ctx.channel.mention} was banished**"
            moderation_embed.description = moderation_embed.description + f"\n\nMessage: {ctx.content}\n"
            moderation_embed.description = moderation_embed.description + f"Detected banished word: {args[1]}\n"
            moderation_embed.color = discord.Color.red()

            moderation_embed.timestamp = datetime.utcnow()
            moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            moderation_embed.set_footer(text=f"Author: {user.id} | Message ID: {ctx.id}")
            
            await ctx.reply(f"{args[0]}")
            await audit.send(embed=moderation_embed)
            bot.logger.info(f"\n{ctx.author.name}'s message was banished.\nMessage: {ctx.content}\nDetected word: {args[1]}")

            return

        if isGud:
            await user.send(embed=moderation_embed)

    async def log_command(bot, author: discord.User, ctx: Context):
        # if SemiConfig.feature_enabled("command_used_log")

        logged_commands = SemiConfig.get_config_wild(commands, file_name="logged")
        message_content = ctx.message.content
        interaction = ctx.interaction

        if interaction == None:
            bot.logger.info(msg=f"{author}: {message_content}")
        else:
            content = f"/{interaction.command.name}"

            if len(interaction.command.parameters) > 0:
                for option in interaction.data["options"]:
                    content = f"{content} {option['name']}: {option['value']}"
                    # content = f"{content} {option['value']}"
                
            bot.logger.info(msg=f"{interaction.user.name}: {content}")
            if interaction.command.name in logged_commands:
                audit = ctx.guild.get_channel(await SemiBot.get_channel_id(ctx, "audit"))
                moderation_embed = bot.create_embed_notitle()

                moderation_embed.description = f"Used `{interaction.command.name}` command in <#{ctx.channel.id}>"
                moderation_embed.description = f"{moderation_embed.description}\n{content}"
                moderation_embed.color = discord.Color.blue()

                moderation_embed.timestamp = datetime.utcnow()
                moderation_embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)

                await audit.send(embed=moderation_embed)
                # moderation_embed.set_footer(text=f"Bot developed by snow2code")

    def get_user_nick(user: Union[discord.User, discord.Member]):
        nick = user.display_name
        errors = []
        if isinstance(user, discord.Member):
            if user.nick != None:
                nick = user.nick

        # 22/03/2026 (EU) - Prevent AFK status "stacking"
        if nick.find("[AFK] ") >= 0:
            nick = nick.replace("[AFK] ", "")
            
        # Discord's nickname character limit is 32.
        # - we need 6 character for the AFK nickname
        if len(nick) > 26:
            errors.append("I cannot put 'AFK' in your nickname because of the nickname character limit. (32 max.)")

        # Servers - We can't change the server owner's nick.
        if isinstance(user, discord.Member):
            if user.id == user.guild.owner_id:
                errors.append("I cannot change your nickname.")

        return {"nick": nick, "errors": errors}

    async def member_number(guild: discord.Guild, member: discord.Member):
        sorted_members = sorted(
            [m for m in guild.members if m.joined_at],
            key=lambda m: m.joined_at
        )

        return sorted_members.index(member) + 1
    
    async def server_configured(ctx: Context):
        server_config = SemiConfig.get_server_config(ctx.guild.id)

        if server_config == None:
            return False
        return True
    
    async def get_channel_id(ctx: Context, name: str):
        server_config = SemiConfig.get_server_config(ctx.guild.id)

        if server_config == None:
            await ctx.reply("The server owner needs to configure the server!")
            await ctx.channel.guild.owner.send(f'You need to configure your server *"{ctx.guild.name}"*\n\nSet ***ALL*** channels in the set_channel_id command. (like /set_channel_id audit #channel)\n\nThis was caused because {name} is not configured in the server.')
        else:
            try:
                channel_ids = server_config['server_ids']
                return channel_ids[name]
            except KeyError as e:
                await ctx.reply("The server owner needs to configure the server!")
                await ctx.channel.guild.owner.send(f'You need to configure your server *"{ctx.guild.name}"*\n\nSet ***ALL*** channels in the set_channel_id command. (like /set_channel_id audit #channel)\n\nThis was caused because {name} is not configured in the server.. orr because: {e}')
                    
        return None

    async def get_channel_id_2(guild: discord.Guild, name: str):
        server_config = SemiConfig.get_server_config(guild.id)

        if server_config == None:
            pass
        else:
            try:
                channel_ids = server_config['server_ids']
                return channel_ids[name]
            except KeyError as e:
                pass
                    
        return None
    
    async def get_role_id(ctx: Context, name: str):
        server_config = SemiConfig.get_server_config(ctx.guild.id)

        if server_config == None:
            await ctx.reply("The server owner needs to configure the bot for the server!")
            await ctx.channel.guild.owner.send(f'You need to configure your server *"{ctx.guild.name}"*\n\nSet ***ALL*** channels in the set_channel_id command. (like /set_channel_id audit #channel)\n\nThis was caused because {name} is not configured in the server.')
        else:
            try:
                role_ids = server_config['role_ids']
                return role_ids[name]
            except KeyError as e:
                await ctx.reply("The server owner needs to configure the bot for the server!")
                await ctx.channel.guild.owner.send(f'You need to configure your server *"{ctx.guild.name}"*\n\nSet ***ALL*** channels in the set_channel_id command. (like /set_channel_id audit #channel)\n\nThis was caused because {name} is not configured in the server.. orr because: {e}')
                    
        return None

    def command_disabled(ctx: Context):
        disabled = SemiConfig.get_config_wild("commands", file_name="disabled")

        try:
            cmd_name = ""

            if ctx.interaction == None:
                cmd_name = ctx.command.name
            else:
                cmd_name = ctx.interaction.command.name

            if cmd_name in disabled:
                return True
        except KeyError:
            return False
        # commands = files.get_filepath("commands", "json")
        # disabled = None

        # with open(commands, "r", encoding="utf8") as file:
        #     data = json.load(file)
        #     disabled = data['disabled']

        # if ctx.interaction == None:
        #     if ctx.command.name in disabled:
        #         return True
        # else:
        #     if ctx.interaction.command.name in disabled:
        #         return True

        # return False