###############################################
#
# File: listeners.database.
# Date: 10/05/2026 (EU)
# Date Edited: 
# Project: Fluffy Concourse - Fluffy Helper Bot
# Purpose: 
#  
# Author: snow2code
#
###############################################


from discord.ext import commands
from utils.semibot import Bot
from utils.globals import Globals
from utils.semidata import SemiData

from cogs.server_owner_n_bot_dev.config.features import Features
from cogs.server_owner_n_bot_dev.config.channels import Channels
from cogs.server_owner_n_bot_dev.config.roles import Roles

class Database_MakeServerConfig(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # We are ready.. Go through all servers the bot is in
    @commands.Cog.listener()
    async def on_ready(self):
        conn = SemiData.server_config_conn

        for guild in self.bot.guilds:
            # All features enabled by default
            for feature in Features:
                exists = conn.execute(
                    "SELECT EXISTS (SELECT 1 FROM features WHERE server_id = ? AND feature_name = ? LIMIT 1)",
                    (guild.id, feature.value)
                ).fetchone()[0]

                # 1 - Exists
                # 0 - Doesn't exist
                if exists == 0:
                    conn.execute( f'INSERT INTO features VALUES ("{guild.id}", "{feature.name}", 1)' )
                    conn.commit()

            for channel in Channels:
                exists = conn.execute(
                    "SELECT EXISTS (SELECT 1 FROM channel_ids WHERE server_id = ? AND channel_name = ? LIMIT 1)",
                    (guild.id, channel.value)
                ).fetchone()[0]

                # 1 - Exists
                # 0 - Doesn't exist
                if exists == 0:
                    conn.execute( f'INSERT INTO channel_ids VALUES ("{guild.id}", "{channel.name}", 1)' )
                    conn.commit()

            for role in Roles:
                exists = conn.execute(
                    "SELECT EXISTS (SELECT 1 FROM role_ids WHERE server_id = ? AND role_name = ? LIMIT 1)",
                    (guild.id, role.value)
                ).fetchone()[0]

                # 1 - Exists
                # 0 - Doesn't exist
                if exists == 0:
                    conn.execute( f'INSERT INTO role_ids VALUES ("{guild.id}", "{role.name}", NULL)' )
                    conn.commit()

        pass

async def setup(bot):
    await bot.add_cog(Database_MakeServerConfig(bot))
