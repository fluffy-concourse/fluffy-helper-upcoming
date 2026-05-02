###############################################
#
# File: utils.config
# Date: 22/04/2026 (EU)
# Author: snow2code
#
###############################################


import os
import json
import discord
import asyncio
from typing import Union

def get_path(argpath):
    if len(argpath) > 0:
        path = ""
        for i, dir in enumerate(argpath):
            path_length = len(argpath) - 1
            if i == path_length:
                # Do not add a "/" to the end of the path
                path += f"{dir}"
            else:
                path += f"{dir}/"
        return f"_config/{path}"
    return f"_config"


class SemiConfig():
    def __init__(self):
        self.lock = asyncio.Lock()

    def in_radar_force(id: int, radar: str):
        forced = SemiConfig.get_config_wild( "radar",   file_name="forced" )

        try:
            if forced[radar][id]:
                return True
        except KeyError:
            return False

    def in_radar_ignore(id: int, radar: str):
        ignore = SemiConfig.get_config_wild( "radar",   file_name="ignore" )

        try:
            if ignore[radar][id]:
                return True
        except KeyError:
            return False

    def feature_enabled(server_id: int, name: str):
        server_config = SemiConfig.get_server_config(server_id)

        if server_config == None:
            return False
        else:
            if name in server_config['features']:
                return server_config['features'][name]
                    
        return False
    
    def get_config(file_name: str):
        if os.path.exists(f'_config/{file_name}.json'):
            path = os.path.abspath(f'_config/{file_name}.json')
            file = open(path, 'r', encoding='utf8')

            return json.loads(file.read())
        return ['File not found']

    def get_config_wild(*argpath, file_name: str):
        path = get_path(argpath)

        if os.path.exists(f'_config/{path}/{file_name}.json'):
            path = os.path.abspath(f'{path}/{file_name}.json')
            file = open(path, 'r', encoding='utf8')

            return json.loads(file.read())
        return ['File not found']
    

    def get_server_config(server_id: Union[int, discord.Guild]):
        if os.path.exists(f"_config/server/{server_id}"):
            file = open(f"_config/server/{server_id}", 'r', encoding='utf8')
            
            return json.loads(file.read())

