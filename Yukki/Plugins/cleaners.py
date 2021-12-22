from Yukki import app, OWNER
from pyrogram import filters, Client
from pyrogram.types import Message
from ..YukkiUtilities.helpers.filters import command
import subprocess
import shutil
import os


@Client.on_message(command("clean") & filters.user(OWNER))
async def clear_storage(_, message: Message):   
    dir0 = 'downloads'
    dir1 = 'raw_files'
    dir2 = 'search'
    shutil.rmtree(dir0)
    shutil.rmtree(dir1)
    shutil.rmtree(dir2)
    os.mkdir(dir0)
    os.mkdir(dir1)
    os.mkdir(dir2)
    await message.reply_text("✅ Cleaned all **temp** dir(s)")
