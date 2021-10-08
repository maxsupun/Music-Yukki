from Yukki import app, SUDOERS
from pyrogram import filters, Client
from pyrogram.types import Message
from ..YukkiUtilities.helpers.filters import command
import subprocess
import shutil
import os
   
    
@Client.on_message(command("clean") & filters.user(SUDOERS))
async def storagefree(_, message: Message):   
    dir0 = 'downloads'
    dir1 = 'raw_files'
    dir2 = 'search'
    shutil.rmtree(dir0)
    shutil.rmtree(dir1)
    shutil.rmtree(dir2)
    os.mkdir(dir0)
    os.mkdir(dir1)
    os.mkdir(dir2)
    await message.reply_text("✅ Cleaned all **temp** directories!")
