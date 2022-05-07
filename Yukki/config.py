import os
from os import getenv
from dotenv import load_dotenv

load_dotenv() # environment

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
SESSION_NAME = getenv("SESSION_NAME", "session")

ASS_ID = int(getenv("ASS_ID"))
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID"))
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "54000"))
OWNER_ID = list(map(int, getenv("OWNER_ID", "1757169682").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! . $").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1757169682").split()))
