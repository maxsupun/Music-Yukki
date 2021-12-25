from Yukki import app, OWNER
from pyrogram import filters, Client
from pyrogram.types import Message
from ..YukkiUtilities.helpers.filters import command
import subprocess
import shutil
import os
   
    
@Client.on_message(command("clean") & filters.user(OWNER))
async def clear_storage(_, message: Message):    
    dir = 'downloads'
    dir1 = 'search'
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("✅ Cleaned all **temp** dir(s) !")
