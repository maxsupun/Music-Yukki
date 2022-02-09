import os
import time
from os import path
import random
import asyncio
import shutil
from pytube import YouTube
from yt_dlp import YoutubeDL
from .. import converter
import yt_dlp
import shutil
import psutil
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import Voice
from sys import version as pyver
from Yukki import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from Yukki.YukkiUtilities.database.onoff import (is_on_off, add_on, add_off)
from Yukki.YukkiUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats)
from ..YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup, play_list_keyboard)
from Yukki.YukkiUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Yukki.YukkiUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from ..config import DURATION_LIMIT
from ..YukkiUtilities.helpers.decorators import errors
from ..YukkiUtilities.helpers.filters import command, other_filters
from ..YukkiUtilities.helpers.gets import (get_url, themes, random_assistant, ass_det)
from ..YukkiUtilities.helpers.logger import LOG_CHAT
from ..YukkiUtilities.helpers.thumbnails import down_thumb
from ..YukkiUtilities.helpers.chattitle import CHAT_TITLE
from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from pyrogram import filters
from typing import Union
import subprocess
from asyncio import QueueEmpty
import shutil
import os
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, )
flex = {}
chat_watcher_group = 3
def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )


@Client.on_message(command(["music", "song"]) & other_filters)
async def musicdl(_, message: Message):
    await message.delete()
    chat_id = message.chat.id
    if not await is_served_chat(chat_id):
        await message.reply(f"❌ **This chat not authorized !**\n\nI can't stream music in non-authorized chat, ask to sudo user to auth this chat.\n\nCheck the sudo user list [From Here](https://t.me/{BOT_USERNAME}?start=sudolist)", disable_web_page_preview=True)
        return await app.leave_chat(chat_id)  
    if message.sender_chat:
        return await message.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")  
    user_id = message.from_user.id
    chat_title = message.chat.title
    username = message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    
    url = get_url(message)
    await message.delete()
    fucksemx = 0
    if url:
        query = " ".join(message.command[1:])
        mystic = await _.send_message(chat_id, "🔍 **Searching...**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = (result["title"])
                duration = (result["duration"])
                views = (result["viewCount"]["short"])  
                thumbnail = (result["thumbnails"][0]["url"])
                link = (result["link"])
                idxz = (result["id"])
                videoid = (result["id"])
        except Exception as e:
            return await mystic.edit_text("😕 Sorry, we **couldn't** find the song you were looking for\n\n• Check that the **name is correct** or **try by searching the artist.**")    
        smex = int(time_to_seconds(duration))
        if smex > DURATION_LIMIT:
            return await mystic.edit_text(f"**__Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)")
        if duration == "None":
            return await mystic.edit_text("❌ **live stream not supported**")
        if views == "None":
            return await mystic.edit_text("❌ **live stream not supported**")
        thumb = await down_thumb(thumbnail, user_id)
        buttons = gets(videoid, user_id)
        m = await message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),    
            caption=(f"🏷 <b>Name:</b> [{title[:65]}]({url})\n\n💡 [Check music information](https://t.me/{BOT_USERNAME}?start=info_{id})")
        )   
        os.remove(thumb)
    else:
        if len(message.command) < 2:
            await message.reply_text("**usage:**\n\n/song or /music [yt url/music name]")
        query = " ".join(message.command[1:])
        mystic = await _.send_message(chat_id, "🔍 **Searching...**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = (result[0]["title"])
            duration1 = (result[0]["duration"])
            title2 = (result[1]["title"])
            duration2 = (result[1]["duration"])      
            title3 = (result[2]["title"])
            duration3 = (result[2]["duration"])
            title4 = (result[3]["title"])
            duration4 = (result[3]["duration"])
            title5 = (result[4]["title"])
            duration5 = (result[4]["duration"])
            ID1 = (result[0]["id"])
            ID2 = (result[1]["id"])
            ID3 = (result[2]["id"])
            ID4 = (result[3]["id"])
            ID5 = (result[4]["id"])
        except Exception as e:
            return await mystic.edit_text("😕 Sorry, we **couldn't** find the song you were looking for\n\n• Check that the **name is correct** or **try by searching the artist.**")
        thumb ="cache/results.png"
        link = "https://www.youtube.com/watch?v={id}"
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await mystic.edit(
            f"• Choose the results to download !\n\n1️⃣ <b>[{title1[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n\n2️⃣ <b>[{title2[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n\n3️⃣ <b>[{title3[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n\n4️⃣ <b>[{title4[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n\n5️⃣ <b>[{title5[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID5})",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return
    
    
@Client.on_callback_query(filters.regex(pattern=r"beta"))
async def download_data(_,CallbackQuery): 
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        id,duration,user_id = callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"❌ an error occured\n\n**reason:** `{e}`")
    if duration == "None":
        return await CallbackQuery.message.reply_text(f"❌ **live stream not supported**")      
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer("💡 sorry this is not your request", show_alert=True)
    await CallbackQuery.message.delete()
    checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    url = (f"https://www.youtube.com/watch?v={id}")
    videoid = id
    idx = id
    smex = int(time_to_seconds(duration))
    if smex > DURATION_LIMIT:
        await CallbackQuery.message.reply_text(f"**❌ __Duration Error__**\n\n**Allowed Duration: **90 minute(s)\n**Received Duration:** {duration} minute(s)")
        return 
    try:
        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
            x = ytdl.extract_info(url, download=False)
    except Exception as e:
        return await CallbackQuery.message.reply_text(f"failed to download this video.\n\n**reason:** `{e}`") 
    title = (x["title"])
    thumbnail = (x["thumbnail"])
    idx = (x["id"])
    videoid = (x["id"])
    thumb = await down_thumb(thumbnail, user_id)
    buttons = gets(videoid, user_id)
    m = await CallbackQuery.message.reply_photo(
        photo=thumb,
        reply_markup=InlineKeyboardMarkup(buttons),    
        caption=(f"🏷 **Name:** [{title[:80]}]({url})\n\n💡 [Check music information](https://t.me/{BOT_USERNAME}?start=info_{id})")
    )   
    os.remove(thumb)
    await CallbackQuery.message.delete()
        
        
@Client.on_callback_query(filters.regex(pattern=r"chonga"))
async def chonga(_,CallbackQuery): 
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    userid = CallbackQuery.from_user.id 
    try:
        id , query, user_id = callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"❌ an error occured\n**reason:** `{e}`")       
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer("💡 sorry this is not your request", show_alert=True)
    i=int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = (result[0]["title"])
        duration1 = (result[0]["duration"])
        title2 = (result[1]["title"])
        duration2 = (result[1]["duration"])      
        title3 = (result[2]["title"])
        duration3 = (result[2]["duration"])
        title4 = (result[3]["title"])
        duration4 = (result[3]["duration"])
        title5 = (result[4]["title"])
        duration5 = (result[4]["duration"])
        title6 = (result[5]["title"])
        duration6 = (result[5]["duration"])
        title7= (result[6]["title"])
        duration7 = (result[6]["duration"])      
        title8 = (result[7]["title"])
        duration8 = (result[7]["duration"])
        title9 = (result[8]["title"])
        duration9 = (result[8]["duration"])
        title10 = (result[9]["title"])
        duration10 = (result[9]["duration"])
        ID1 = (result[0]["id"])
        ID2 = (result[1]["id"])
        ID3 = (result[2]["id"])
        ID4 = (result[3]["id"])
        ID5 = (result[4]["id"])
        ID6 = (result[5]["id"])
        ID7 = (result[6]["id"])
        ID8 = (result[7]["id"])
        ID9 = (result[8]["id"])
        ID10 = (result[9]["id"])                    
    except Exception as e:
        return await mystic.edit_text(f"song not found.\n**reason:** {e}")
    if i == 1:
        link = "https://www.youtube.com/watch?v={id}"
        buttons = search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query)
        await CallbackQuery.edit_message_text(
            f"• Choose the results to download !\n\n6️⃣ <b>[{title6[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID6})\n\n7️⃣ <b>[{title7[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID7})\n\n8️⃣ <b>[{title8[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID8})\n\n9️⃣ <b>[{title9[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID9})\n\n🔟 <b>[{title10[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID10})",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return    
    if i == 2:
        link = "https://www.youtube.com/watch?v={id}"
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await CallbackQuery.edit_message_text(
            f"• Choose the results to download !\n\n1️⃣ <b>[{title1[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID1})\n\n2️⃣ <b>[{title2[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID2})\n\n3️⃣ <b>[{title3[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID3})\n\n4️⃣ <b>[{title4[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID4})\n\n5️⃣ <b>[{title5[:30]}...]({link})</b>\n └ 💡 [More information](https://t.me/{BOT_USERNAME}?start=info_{ID5})",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        return    
      

def search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="1️⃣", callback_data=f'beta {ID1}|{duration1}|{user_id}'),
                InlineKeyboardButton(text="2️⃣", callback_data=f'beta {ID2}|{duration2}|{user_id}'),
                InlineKeyboardButton(text="3️⃣", callback_data=f'beta {ID3}|{duration3}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="4️⃣", callback_data=f'beta {ID4}|{duration4}|{user_id}'),
                InlineKeyboardButton(text="5️⃣", callback_data=f'beta {ID5}|{duration5}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="➡️", callback_data=f'chonga 1|{query}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}")
            ],
        ]
    return buttons   

def search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="6️⃣", callback_data=f'beta {ID6}|{duration6}|{user_id}'),
                InlineKeyboardButton(text="7️⃣", callback_data=f'beta {ID7}|{duration7}|{user_id}'),
                InlineKeyboardButton(text="8️⃣", callback_data=f'beta {ID8}|{duration8}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="9️⃣", callback_data=f'beta {ID9}|{duration9}|{user_id}'),
                InlineKeyboardButton(text="🔟", callback_data=f'beta {ID10}|{duration10}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="⬅️", callback_data=f'chonga 2|{query}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}")
            ],
        ]
    return buttons     
      
def gets(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="⬇️ Get Audio", callback_data=f'gets audio|{videoid}|{user_id}'),
                InlineKeyboardButton(text="⬇️ Get Video", callback_data=f'gets video|{videoid}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="🗑 Close", callback_data=f'close2')
            ],
        ]
    return buttons
