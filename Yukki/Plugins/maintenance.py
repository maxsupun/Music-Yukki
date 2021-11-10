from Yukki import app, SUDOERS
from pyrogram import filters, Client
from pyrogram.types import Message
from Yukki.YukkiUtilities.database.onoff import (is_on_off, add_on, add_off)
from ..YukkiUtilities.helpers.filters import command


@Client.on_message(command("maintenance") & filters.user(SUDOERS))
async def smex(_, message):
    usage = "**usage:**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("✅ maintenance mode enabled\n\n• from now on, user can't play music after the maintenance mode is disabled.")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("❌ maintenance mode disabled\n\n• from now on, user can play music again.")
    else:
        await message.reply_text(usage)

        
@Client.on_message(command("sptest") & filters.user(SUDOERS))
async def sls_skfs(_, message):
    usage = "**usage:**\n/speedtest [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 2
        await add_on(user_id)
        await message.reply_text("✅ **speedtest enabled**")
    elif state == "disable":
        user_id = 2
        await add_off(user_id)
        await message.reply_text("❌ **speedtest disabled**")
    else:
        await message.reply_text(usage)
