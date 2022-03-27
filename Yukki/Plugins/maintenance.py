from Yukki import app, SUDOERS
from ..YukkiUtilities.helpers.filters import command
from Yukki.YukkiUtilities.database.onoff import add_on, add_off

from pyrogram.types import Message
from pyrogram import filters, Client


@Client.on_message(command("maintenance") & filters.user(SUDOERS))
async def maintenance_off_on(_, message):
    usage = "**usage:**\n\n/maintenance [on / off]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("✅ The maintenance mode is enabled!\n\n• From now on user can't play music until the maintenance period is over.")
    elif state == "off":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("❌ The maintenance mode is disabled!\n\n• From now on all user can play music again.")
    else:
        await message.reply_text(usage)

        
@Client.on_message(command("speedtest") & filters.user(SUDOERS))
async def speedtest_off_on(_, message):
    usage = "**usage:**\n\n/speedtest [on / off]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        user_id = 2
        await add_on(user_id)
        await message.reply_text("✅ **speedtest enabled**")
    elif state == "off":
        user_id = 2
        await add_off(user_id)
        await message.reply_text("❌ **speedtest disabled**")
    else:
        await message.reply_text(usage)
