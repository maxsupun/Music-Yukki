from Yukki import app, OWNER
import os
import subprocess
import shutil
import re
import sys
import traceback
from Yukki.YukkiUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo, add_sudo)
from pyrogram import filters, Client
from pyrogram.types import Message


@app.on_message(filters.command("addsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("reply to a user's message or give username/user_id")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user 
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("✅ already a **sudo user**")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(f"✅ added **{user.mention}** to sudo user list !")
            return os.execvp("python3", ["python3", "-m", "Yukki"])
        await edit_or_reply(message, text="something wrong happened, check logs.")  
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("✅ already a **sudo user**")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"✅ added **{mention}** sudo user list !")
        return os.execvp("python3", ["python3", "-m", "Yukki"])
    await edit_or_reply(message, text="something wrong happened, check logs.")  
    return    
          
              
@app.on_message(filters.command("delsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("reply to a user's message or give username/user_id.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user      
        if user.id not in await get_sudoers():
            return await message.reply_text(f"❌ user is not a part of veez mega")        
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"✅ removed **{user.mention}** from sudo user list")
            return os.execvp("python3", ["python3", "-m", "Yukki"])
        await message.reply_text(f"something wrong happened, check logs.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"❌ user is not a part of **veez mega**")        
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"✅ removed **{mention}** from sudo user list")
        return os.execvp("python3", ["python3", "-m", "Yukki"])
    await message.reply_text(f"something wrong happened, check logs.")
                
                          
@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "🧙🏻‍♂️ **List of sudo users:**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:                     
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue                     
        text += f"➤ {user}\n"
    if not text:
        await message.reply_text("❌ no sudo users found")  
    else:
        await message.reply_text(text) 
