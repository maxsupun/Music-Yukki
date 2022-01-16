print("[INFO]: STARTING CLIENT :: STAND BY !!")

import time
import logging
import aiohttp
import asyncio
import uvloop
import importlib
from Yukki import config
from logging import getLogger
from pyrogram import Client, idle
from pyrogram import Client as Bot
from aiohttp import ClientSession
from Yukki.config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from Yukki.config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID, OWNER_ID
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

def initialize():
    global dbb
    dbb = {}
    
initialize()

print("[INFO]: INITIALIZING DATABASE")

LOGS = getLogger(__name__)

__version__ = "5.0.0"

MONGODB_CLI = MongoClient(MONGO_DB_URI)
db = MONGODB_CLI.wbb
SUDOERS = SUDO_USERS
OWNER = OWNER_ID
async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDO USERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS
    print("[INFO]: LOADED SUDO USERS")
loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())
YUKKI_START_TIME = time.time()
loop = asyncio.get_event_loop()


BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
ASSID = 0
ASSNAME = ""
ASSUSERNAME = ""
ASSMENTION = ""
print("[INFO]: INITIALIZING BOT CLIENT")
app = Client(
    'mega',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
)
aiohttpsession = ClientSession()

chacha = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)

def all_info(app, chacha):
    global BOT_ID, BOT_NAME, BOT_USERNAME
    global ASSID, ASSNAME, ASSMENTION, ASSUSERNAME
    getme = app.get_me()
    getme1 = chacha.get_me()
    BOT_ID = getme.id
    ASSID = getme1.id
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    ASSNAME = (
        f"{getme1.first_name} {getme1.last_name}"
        if getme1.last_name
        else getme1.first_name
    )
    ASSUSERNAME = getme1.username
    ASSMENTION = getme1.mention

    
print("[INFO]: STARTING TELEBOT CLIENT")
app.start()
print("[INFO]: STARTING USERBOT CLIENT")
chacha.start()
print("[INFO]: GENERATING BOT/ASSISTANT PROFILE INFO")
all_info(app, chacha)
print("[INFO]: GENERATED- BOT/ASSISTANT PROFILE INFO")
