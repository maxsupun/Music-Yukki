from pyrogram import filters, Client
from pyrogram.types import Message
from Yukki import app, SUDOERS, YUKKI_START_TIME
import os
import psutil
import time
from datetime import datetime
from ..YukkiUtilities.helpers.time import get_readable_time

async def bot_sys_stats():
    bot_uptime = int(time.time() - YUKKI_START_TIME)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f'''
» uptime: {get_readable_time((bot_uptime))}
» CPU: {cpu}%
» RAM: {mem}%
» DISK: {disk}%'''
    return stats


@app.on_message(filters.command(["ping", "ping@VeezMegaBot"]))
async def ping(_, message):
    uptime = await bot_sys_stats()
    start = datetime.now()
    response = await message.reply_photo(
        photo="cache/ping.png",
        caption=">> pong !"
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await response.edit_text(f"🏓 `PONG!`\n⚡ `{resp}` ms\n\n🖥 System Stats:\n{uptime}")  
