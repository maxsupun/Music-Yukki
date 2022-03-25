import os
import shutil

from Yukki import OWNER
from pyrogram.types import Message
from pyrogram import filters, Client
from ..YukkiUtilities.helpers.filters import command
   
    
@Client.on_message(command("clean") & filters.user(OWNER))
async def clear_storage(_, message: Message):    
    dir_1 = 'downloads'
    dir_2 = 'search'
    shutil.rmtree(dir_1)
    shutil.rmtree(dir_2)
    os.mkdir(dir_1)
    os.mkdir(dir_2)
    await message.reply_text("✅ Cleaned all **temp** dir(s) !")
