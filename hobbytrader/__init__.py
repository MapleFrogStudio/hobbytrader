import os
from dotenv import load_dotenv
load_dotenv()


FMPAD_API_KEY = os.getenv('FMPAD_API_KEY')

# Sanity loading in case environment variable is not defined
try:
    DB_SQL_LIMIT = abs(int(os.getenv('DB_SQL_LIMIT') if not None else None))
    if DB_SQL_LIMIT != 0:
        print(f'DEBUG: SQL requests limited to {DB_SQL_LIMIT}')
except:
    DB_SQL_LIMIT = 0