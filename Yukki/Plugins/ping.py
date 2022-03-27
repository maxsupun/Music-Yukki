import os
import time
import psutil

from datetime import datetime
from pyrogram.types import Message
from pyrogram import filters, Client

from Yukki import app, YUKKI_START_TIME
from ..YukkiUtilities.helpers.time import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - YUKKI_START_TIME)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f'''
» Uptime: {get_readable_time((bot_uptime))}
» CPU: {cpu}%
» RAM: {mem}%
» DISK: {disk}%'''
    return stats


@app.on_message(filters.command(["ping", "server"]) & ~filters.edited)
async def ping(_, message):
    response = await message.reply_photo(
        photo="cache/ping.png",
        caption=">> pinging..."
    )
    uptime = await bot_sys_stats()
    start = datetime.now()
    stops = datetime.now()
    resp = (stops - start).microseconds / 1000
    await response.edit_text(f"🏓 PONG !\n⏱ `{resp}` ms\n\n🖥 System Stats:\n{uptime}")
