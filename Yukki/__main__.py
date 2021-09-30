import asyncio
import time
import uvloop
import importlib
from pyrogram import Client as Bot, idle
from .config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID
from Yukki import BOT_NAME, ASSNAME, app, chacha, aiohttpsession
from Yukki.YukkiUtilities.database.functions import clean_restart_stage
from Yukki.YukkiUtilities.database.queue import (get_active_chats, remove_active_chat)
from .YukkiUtilities.tgcallsrun import run
from pyrogram import Client, idle
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import time

Bot(
    ':yukki:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Yukki.Plugins'},
).start()


print(f"[INFO]: BOT STARTED AS {BOT_NAME}!")
print(f"[INFO]: ASSISTANT STARTED AS {ASSNAME}!")



async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[INFO]: SENDING RESTART STATUS")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted the Bot Successfully.**",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        print("Error came while clearing db")
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)                                         
        except Exception as e:
            print("Error came while clearing db")
            pass     
    await app.send_message(LOG_GROUP_ID, "Bot Started")
    await chacha.send_message(LOG_GROUP_ID, "Assistant Started")
    print("[INFO]: STARTED")
    
   
loop = asyncio.get_event_loop()
loop.run_until_complete(load_start())

run()
loop.close()

print("[LOG] CLOSING BOT")
