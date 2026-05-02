###############################################
#
# File: utils.semidata
# Date: 23/04/2026 (EU)
# Author: snow2code
#
###############################################


import os
import asyncio
import sqlite3

databases = {
    "banished": [
        {"table_name": "banished_ids", "data": "user_id INT"},
        {"table_name": "banished_words_bypasses", "data": "bypass TEXT"},
        {"table_name": "banished_flagmsg", "data": "word TEXT"},
        {"table_name": "banished_words_noignore", "data": "word TEXT, message TEXT"},
        {"table_name": "banished_words", "data": "word TEXT, message TEXT"},
    ],
    # "other_stuff": [
    #     {"table_name": "jobs", "data": "id INTEGER, job TEXT, wage REAL"}
    # ],
    "user_data": [
        # {"table_name": "radar_values", "data": "user_id INT, amount INT, type TEXT"},
        {"table_name": "afk_users", "data": "user_id INT, server_id INT, name TEXT, message TEXT, since TEXT, toggle INT"},
        {"table_name": "cooldowns", "data": "user_id INT, since TEXT"},
        {"table_name": "user_data", "data": "used INT, user_id INT, server_id INT, alise TEXT, job TEXT, tokens INT, wallet INT, bank INT"}
    ],
    # "moderation": [
    #     {
    #         "table_name": "cases",
    #         "data": "id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INT, staff TEXT, type TEXT, reason TEXT, issued TEXT, expires TEXT"
    #     }
    # ],
    "selfroles": [
        {
            "table_name": "reaction_roles",
            "data": "id INTEGER PRIMARY KEY AUTOINCREMENT, emoji TEXT, emoji_id INT, channel_id INT, role_id INT"
        }
    ]
}

class SemiData():

    @classmethod
    def init(cls):
        ## Create databases
        if not os.path.exists(f"data"):
            os.mkdir("data")
        
        for database in databases:
            # Exists? Check if all tables exist.
            if os.path.exists(f"data/{database}.db"):
                conn = sqlite3.connect(f"data/{database}.db")
                cursor = conn.cursor()

                for table in databases[database]:
                    cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table['table_name']}'")
                    
                    if cursor.fetchone()[0] < 1:
                        conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")

                conn.close()
            else:
                conn = sqlite3.connect(f"data/{database}.db")

                for table in databases[database]:
                    conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")
                    ## 21/03/2026 (EU) - kmskmskmskms
                    # if table["table_name"] == "jobs":
                    #     conn.execute(f'CREATE TABLE {table['table_name']} ({table['data']}) (PRIMARY KEY("id" AUTOINCREMENT))')
                    # else:
                    #     conn.execute(f"CREATE TABLE {table['table_name']} ({table['data']})")
                
                conn.close()
        
        cls.banished_conn = sqlite3.connect(f"data/banished.db", timeout=30, check_same_thread=False)
        cls.jobs_conn = sqlite3.connect(f"data/jobs.db", timeout=30, check_same_thread=False)
        cls.userdata_conn = sqlite3.connect(f"data/user_data.db", timeout=30, check_same_thread=False)
        # cls.moderation_conn = sqlite3.connect(f"data/moderation.db", timeout=30, check_same_thread=False)
        cls.selfroles_conn = sqlite3.connect(f"data/selfroles.db", timeout=30, check_same_thread=False)
        
        cls.banished_conn.execute("PRAGMA journal_mode=WAL;")
        cls.jobs_conn.execute("PRAGMA journal_mode=WAL;")
        cls.userdata_conn.execute("PRAGMA journal_mode=WAL;")
        # cls.moderation_conn.execute("PRAGMA journal_mode=WAL;")
        cls.selfroles_conn.execute("PRAGMA journal_mode=WAL;")
        
    banished_conn = None
    jobs_conn = None
    userdata_conn = None
    # moderation_conn = None
    selfroles_conn = None

    write_lock = asyncio.Lock()

    # def get_cases():
    #     cursor = SemiData.moderation_conn.cursor()

    #     cursor.execute("SELECT * FROM cases")
    #     cases_raw = cursor.fetchall()

    #     result = {
    #         "cases": []
    #     }

    #     for case in cases_raw:
    #         result['cases'].append({
    #             'id': case[0],
    #             'user_id': case[1],
    #             'staff': case[2],
    #             'reason': case[3],
    #             'issed': case[4],
    #             'expires': case[4]
    #         })
        
    #     return result
    
    def get_self_roles():
        cursor = SemiData.selfroles_conn.cursor()

        cursor.execute("SELECT * FROM reaction_roles")
        selfroles_raw = cursor.fetchall()

        result = {
            "roles": []
        }

        for role in selfroles_raw:
            result['roles'].append({
                'id': role[0],
                'emoji': role[1],
                'emoji_id': role[2],
                'channel_id': role[3],
                'role_id': role[4]
            })

        return result
    

    def get_jobs():
        cursor = SemiData.jobs_conn.cursor()

        cursor.execute("SELECT * FROM jobs ORDER BY job ASC")
        jobs_raw = cursor.fetchall()

        result = {
            "jobs": []
        }

        for job in jobs_raw:
            result["jobs"].append({
                "job": job[1],
                "wage": job[2]
            })
            
        return result

    # def get_radar_values():
    #     cursor = SemiData.userdata_conn.cursor()

    #     cursor.execute("SELECT * FROM radar_values")
    #     values_raw = cursor.fetchall()

    #     result = {
    #         "values": []
    #     }

    #     for value in values_raw:
    #         result["values"].append({
    #             "user_id": value[0],
    #             "amount": value[1],
    #             "type": value[2],
    #         })
        
    #     return result

    def get_afks(server_id: int):
        cursor = SemiData.userdata_conn.cursor()

        cursor.execute(f"SELECT * FROM afk_users WHERE server_id={server_id}")
        users_raw = cursor.fetchall()

        result = {
            "users": []
        }

        for user in users_raw:
            result['users'].append({
                'user_id': user[0],
                'name': user[1],
                'message': user[2],
                'since': user[3]
            })

        return result
    
    def get_banished():
        cursor = SemiData.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_ids")
        resultBanishedIds = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_bypasses")
        resultBypassesRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_flagmsg")
        resultFlagMsgRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_noignore")
        resultNoIgnoreRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words")
        resultBanishedWordsRaw = cursor.fetchall()

        result = {
            "ids": [],
            "bypasses": [],
            "flagmsg": [],
            "noignore": {},
            "words": {}
        }

        for id in resultBanishedIds:
            result['ids'].append(id[0])
        for bypass in resultBypassesRaw:
            result['bypasses'].append(bypass[0])
        for flag in resultFlagMsgRaw:
            result['flagmsg'].append(flag[0])

        for noignore in resultNoIgnoreRaw:
            result["noignore"][noignore[0]] = noignore[1]
        for banished in resultBanishedWordsRaw:
            result["words"][banished[0]] = banished[1]
        
        return result
