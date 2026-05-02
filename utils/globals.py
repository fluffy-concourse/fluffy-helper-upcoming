###############################################
#
# File: utils.globals
# Date: 23/04/2026 (EU)
# Author: snow2code
#
###############################################


import random
import discord
from utils.semidata import SemiData
from utils.semibot import Bot, SemiBot, Context
from utils.config import SemiConfig

from datetime import datetime

class Globals():

    banished_ids = None
    banished_words_bypasses = None
    banished_flagmsg = None
    banished_words_noignore = None
    banished_words = None

    afk_users = None
    jobs = None

    radar_values = None
    # moderation_cases = None
    selfroles = None

    async def fluffyRadar(bot: Bot, ctx: Context, user: discord.Member, radar: str):
        user_name = SemiBot.get_user_nick(ctx)['nick']
        date = datetime.now().strftime("%d %B")
        emoji = "🎀"
        amount = random.randint(1, 100)

        forced = SemiConfig.get_config_wild("radar", file_name="forced")
        ignore = SemiConfig.get_config_wild("radar", file_name="ignore")
        desc = f"{user.mention} is {amount}% {radar}! {emoji}"

        embed = bot.create_embed(
            title=f"{emoji} {radar.capitalize()} Radar {emoji}",
            color=discord.Color.pink(),
            use_by_snow2code_footer=True
        )

        if radar == "bi":
            if ctx.guild.id == 1414222707570118656:
                emoji = "<:bisexual:1480372668351119611>"
            else:
                emoji = "<:bisexual:1496839929995460679>"
        elif radar == "gay":
            emoji = "🏳️‍🌈"
        elif radar == "queer":
            if ctx.guild.id == 1414222707570118656:
                emoji = "<:queer:1496844579113144432>"
            else:
                emoji = "<:queer:1496844483487338540>"
        # elif radar == "rizz":
        #     pass
        elif radar == "silly":
            if ctx.guild.id == 1414222707570118656:
                emoji = "<:fox_owo:1479235584127143978>"
            else:
                emoji = "<:fox_owo:1496840002162786345>"
        elif radar == "trans":
            if ctx.guild.id == 1414222707570118656:
                emoji = "<:transgender:1480373076238532788>"
            else:
                emoji = "<:transgender:1496839771295711253>"


        if amount == 67:
            if random.randint(1, 2) == 1:
                amount = amount - 1
            else:
                # Use 69.. nice
                amount = amount + 2

        # April Fools Amount
        if date == "01 April":
            fool = True

            try:
                fool = False
                embed.description = f"{user.mention} is 0% {radar}! {emoji}"
            except TypeError:
                pass
            
            try:
                fool = False
                embed.description = f"{user.mention} is 100% {radar}! {emoji}"
            except TypeError:
                pass


            # If radar is silly and the user has silly role, force sillie!
            if radar == "silly":
                silly = SemiBot.get_role_id(user, "silly")

                if user.get_role(silly):
                    fool = False
                    embed.description = f"{user.mention} is 100% {radar}! {emoji}"

            if radar == "cute" and user.id == 888072934114074624:
                fool = True

            if fool:
                _what = ""
                for letter in radar:
                    _what = _what + f" {letter}"

                embed.description = f"{user.mention} is ∞% {radar}! {emoji}\n{user_name} is **I N F I N I T E L Y**  **{_what.upper()}**"

        else:
            if radar == "rizz":
                desc = f"{user.mention} has {amount}% {radar}! {emoji}"
            
            try:
                if user.id in ignore[radar]:
                    desc = f"{user.mention} is 0% {radar}! {emoji}"
            except TypeError:
                pass
            
            try:
                if user.id in forced[radar]:
                    desc = f"{user.mention} is 101% {radar}! {emoji}"
            except TypeError:
                pass


            # If radar is silly and the user has silly role, force sillie!
            if radar == "silly":
                silly = SemiBot.get_role_id(user, "silly")

                if user.get_role(silly):
                    fool = False
                    desc = f"{user.mention} is 100% {radar}! {emoji}"

            if radar == "cute":
                if amount >= 50 and amount < 80:
                    desc = f"{desc}\n{user_name} is totally cute!"
                elif amount >= 80:
                    desc = f"{desc}\n{user_name} is **A D O R A B L E**!"
                    
            elif radar == "silly":
                if amount >= 50 and amount < 80:
                    desc = f"{desc}\n{user_name} is totally silly!"
                elif amount >= 80:
                    desc = f"{desc}\n{user_name} is **T O O  S I L L Y**!"
            elif radar == "gay" and amount >= 50:
                desc = f"{desc}\n{user_name} is totally gay!"
            embed.description = desc
        
        # Globals.update_radar_values(bot.logger)
        return embed


    ## DATABASE
    def is_user_afk(user_id):
        for user in Globals.afk_users:
            if user['user_id'] == user_id:
                return user
            
        return False

    def update_radar_values(logger):
        data = SemiData.get_radar_values()
        logger.info("Updating radar values.")

        Globals.radar_values = data['values']

    def update_banished(logger):
        data = SemiData.get_banished()
        logger.info("Updating banished lists.")

        Globals.banished_ids = {}
        Globals.banished_words_bypasses = {}
        Globals.banished_flagmsg = {}
        Globals.banished_words_noignore = {}
        Globals.banished_words = {}

        Globals.banished_ids = data['ids']
        Globals.banished_words_bypasses = data['bypasses']
        Globals.banished_flagmsg = data['flagmsg']
        Globals.banished_words_noignore = data['noignore']
        Globals.banished_words = data['words']

    def update_jobs(logger):
        data = SemiData.get_jobs()
        logger.info("Updating jobs.")

        Globals.jobs = data['jobs']
        
    def update_afk(logger, server_id: int):
        data = SemiData.get_afks(server_id)
        logger.info("Updating AFK Users.")

        Globals.afk_users = data['users']
        

    # def update_cases(logger):
    #     data = SemiData.get_cases()
    #     logger.info("Updating cases.")

    #     Globals.moderation_cases = {}
    #     Globals.moderation_cases = data['cases']
        
    def update_selfroles(logger):
        data = SemiData.get_self_roles()
        logger.info("Updating self roles.")

        Globals.selfroles = {}
        Globals.selfroles = data['roles']
        
    