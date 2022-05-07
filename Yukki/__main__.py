import time
import uvloop
import asyncio
import importlib

from pytgcalls import idle
from pyrogram import Client

from .YukkiUtilities.tgcallsrun import run as runs
from Yukki import BOT_NAME, ASSNAME, app, chacha, aiohttpsession
from Yukki.YukkiUtilities.database.functions import clean_restart_stage
from Yukki.YukkiUtilities.database.queue import (get_active_chats, remove_active_chat)
from .config import API_ID, API_HASH, BOT_TOKEN, MONGO_DB_URI, SUDO_USERS, LOG_GROUP_ID


Client(
    ':mega:',
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'Yukki.Plugins'},
).start()

print(f"[ INFO ] BOT STARTED AS {BOT_NAME} !")
print(f"[ INFO ] USERBOT STARTED AS {ASSNAME} !")


async def load_start():
    restart_data = await clean_restart_stage()
    if restart_data:
        print("[ SERVER ] <--- RESTARTING CLIENT --->")
        try:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "✅ Bot restarted successfully",
            )
        except Exception:
            pass
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception:
        print("error came while clearing db")
        pass
    for served_chat in served_chats:
        try:
            await remove_active_chat(served_chat)                                         
        except Exception:
            print("error came while clearing db")
            pass     
    await app.send_message(LOG_GROUP_ID, "✅ bot client started")
    await chacha.send_message(LOG_GROUP_ID, "✅ userbot client started")
    print("[ SERVER ] <--- CLIENT RESTARTED! --->")
    
 
loop = asyncio.get_event_loop_policy()
new_event_loop = loop.new_event_loop()
new_event_loop.run_until_complete(load_start())
runs()
idle()

loop.close()
print("[ INFO ] BOT & USERBOT CLIENT STOPPED !")
