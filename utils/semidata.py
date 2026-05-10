###############################################
#
# File: utils.semidata
# Date: 23/04/2026 (EU)
# Date Edited: 10/05/2026 (EU)
# Purpose:
#  
# Author: snow2code
#
###############################################


import os
import asyncio
import sqlite3

databases = {
    "example": [
        {"table_name": "table", "data": "field1 TEXT, field2 TEXT"},
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
                
                conn.close()
        
        # Example.. We'd recommend this (edit banished_conn to be the database name, like "example_conn")
        # cls.banished_conn = sqlite3.connect(f"data/banished.db", timeout=30, check_same_thread=False)
        
        # cls.banished_conn.execute("PRAGMA journal_mode=WAL;")
        
    # banished_conn = None

    write_lock = asyncio.Lock()
