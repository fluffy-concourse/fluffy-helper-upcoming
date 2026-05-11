###############################################
#
# File: utils.config
# Date: 22/04/2026 (EU)
# Date Edited: 10/05/2026 (EU)
# Project: Fluffy Concourse - Fluffy Helper Bot
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import json
import discord
import asyncio
from typing import Union
from utils.semidata import SemiData

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

    def feature_enabled(server_id: int, name: str):
        conn = SemiData.server_config_conn
        features = conn.execute(f"SELECT * FROM features WHERE server_id={server_id}").fetchall()
        
        for feature in features:
            value = bool(feature[2])
            if feature[1] == name:
                return value

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

