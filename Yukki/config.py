##Config

from os import getenv
from dotenv import load_dotenv

load_dotenv()
SESSION_NAME = getenv('SESSION_NAME1', 'session')
SESSION1 = getenv('SESSION_NAME2', 'session')
BOT_TOKEN = getenv('BOT_TOKEN')
API_ID = int(getenv('API_ID', ''))
API_HASH = getenv('API_HASH')
DURATION_LIMIT = int(getenv('DURATION_LIMIT', '10'))
COMMAND_PREFIXES = list(getenv('COMMAND_PREFIXES', '/ !').split())
MONGO_DB_URI = getenv("MONGO_DB_URI")
MONGO_OLD = getenv("MONGO_DB_URI2")
SUDO_USERS = list(map(int, getenv('SUDO_USERS', '').split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", ''))
ASS_ID = int(getenv("ASS_ID", ''))
assnumber = int(getenv('assnumber', ''))
OWNER_ID = list(map(int, getenv('OWNER_ID', '').split()))
