import os
import shutil
import asyncio
import subprocess
from sys import version as pyver
from pyrogram.types import Message
from pyrogram import filters, Client
from pyrogram.errors import FloodWait

from Yukki import app, SUDOERS
from Yukki.YukkiUtilities.database.queue import (get_active_chats, is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def restart_server(_, message):
    A = "downloads"
    B = "raw_files"
    shutil.rmtree(A)
    shutil.rmtree(B)
    await asyncio.sleep(2)
    os.mkdir(A)
    os.mkdir(B)
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for x in served_chats:
        try:
            await app.send_message(
                x,
                f"veez mega server has just restarted.\n\nsorry for the issues, start playing after 15-20 seconds again.",
            )
            await remove_active_chat(x)
        except Exception:
            pass
    x = await message.reply_text(f"restarting veez mega bot.")
    os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_bot(_, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("update found, pushing now !")
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("bot is already up-to-date")


@app.on_message(filters.command("activevc") & filters.user(SUDOERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"error: `{e}`")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await message.reply_text("❌ no active voice chats")
    else:
        await message.reply_text(
            f"💡 **Active voice chats:**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("leavebot") & filters.user(SUDOERS))
async def bot_leave_group(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**usage:**\n\n/leavebot [chat username or chat id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"❌ procces failed\n\nreason: `{e}`")
        print(e)
        return
    await message.reply_text("✅ bot successfully left chat")
