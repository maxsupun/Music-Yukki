import os
import random
import asyncio
import yt_dlp
from os import path
from . import queues
from ... import config
from typing import Dict, Union
from Yukki import BOT_USERNAME
from asyncio import QueueEmpty
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from Yukki import app, BOT_USERNAME
from pyrogram import Client, filters
from Yukki.converter import converter
from Yukki.config import LOG_GROUP_ID
from youtubesearchpython import VideosSearch
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.helpers.inline import play_keyboard
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Yukki.YukkiUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Yukki.YukkiUtilities.helpers.gets import (get_url, themes, random_assistant)
from Yukki.YukkiUtilities.helpers.thumbnails import gen_thumb
from Yukki.YukkiUtilities.helpers.chattitle import CHAT_TITLE
from Yukki.YukkiUtilities.helpers.ytdl import ytdl_opts 
from Yukki.YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Yukki.YukkiUtilities.tgcallsrun import (convert, download)
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import (CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message, Audio, Voice)

flex = {}
smexy = Client(config.SESSION_NAME, config.API_ID, config.API_HASH)
pytgcalls = PyTgCalls(smexy)

@pytgcalls.on_kicked()
async def on_kicked(client: PyTgCalls, chat_id: int) -> None:
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)

     
@pytgcalls.on_closed_voice_chat()
async def on_closed(client: PyTgCalls, chat_id: int) -> None:
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    await remove_active_chat(chat_id)


@pytgcalls.on_stream_end()
async def on_stream_end(client: PyTgCalls, update: Update) -> None:
    chat_id = update.chat_id
    try:
        queues.task_done(chat_id)
        if queues.is_empty(chat_id):
            await remove_active_chat(chat_id)               
            await pytgcalls.leave_group_call(chat_id)
        else:
            afk = queues.get(chat_id)['file']
            f1 = (afk[0])
            f2 = (afk[1])
            f3 = (afk[2])
            finxx = (f"{f1}{f2}{f3}")
            if str(finxx) != "raw":  
                mystic = await app.send_message(chat_id, "📥 downloading next music from playlist...")
                url = (f"https://www.youtube.com/watch?v={afk}")
                ctitle = (await app.get_chat(chat_id)).title
                logger_text=f"""▶ playing music from playlist

Group: `{chat_id}`
Title: {ctitle}

🔗 {url}"""
                okay = await smexy.send_message(LOG_GROUP_ID, f"{logger_text}", disable_web_page_preview=True)
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(f"failed to download this video.\n\n**reason:** {e}") 
                
                chat_title = ctitle                
                videoid = afk
                title = (x["title"])
                def my_hook(d):
                    if d['status'] == 'downloading':
                        percentage = d['_percent_str']
                        per = (str(percentage)).replace(".","", 1).replace("%","", 1)
                        per = int(per)
                        eta = d['eta']
                        speed = d['_speed_str']
                        size = d['_total_bytes_str']
                        bytesx = d['total_bytes']
                        if str(bytesx) in flex:
                            pass
                        else:
                            flex[str(bytesx)] = 1
                        if flex[str(bytesx)] == 1:
                            flex[str(bytesx)] += 1
                            mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                        if per > 500:    
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per > 800:    
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per == 1000:    
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                mystic.edit(f"Downloading {title[:50]}.....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec") 
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                loop = asyncio.get_event_loop()
                xx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xx)
                await pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            file,
                        ),
                    ),
                )
                thumbnail = (x["thumbnail"])
                duration = (x["duration"])
                duration = round(x["duration"] / 60)
                theme = random.choice(themes)
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f'search/{afk}id.txt', 'r')        
                userid =(f2.read())
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                videoid = afk
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                await app.send_photo(chat_id,
                photo= thumb,
                reply_markup=InlineKeyboardMarkup(buttons),    
                caption=(f"🏷 **Name:** {title[:70]}\n⏱ **Duration:** `{duration}` m\n💡 **Status:** `Playing`\n🎧 **Request by:** {semx.mention}")
            )   
                os.remove(thumb)
            else:      
                await pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            afk,
                        ),
                    ),
                )
                _chat_ = ((str(afk)).replace("_","", 1).replace("/","", 1).replace(".","", 1))
                f2 = open(f'search/{_chat_}title.txt', 'r')        
                title =(f2.read())
                f3 = open(f'search/{_chat_}duration.txt', 'r')        
                duration =(f3.read())
                f4 = open(f'search/{_chat_}username.txt', 'r')        
                username =(f4.read())
                f4 = open(f'search/{_chat_}videoid.txt', 'r')        
                videoid =(f4.read())
                user_id = 1
                videoid = str(videoid)
                if videoid == "smex1":
                    buttons = audio_markup(videoid, user_id)
                else:
                    buttons = play_markup(videoid, user_id)
                await app.send_photo(chat_id,
                photo=f"downloads/{_chat_}final.png",
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"🏷 **Name:** {title[:70]}\n⏱ **Duration:** `{duration}` m\n💡 **Status:** `Playing`\n🎧 **Request by:** {username}",
                )
                return
           
    except Exception as e:
        print(e) 


run = pytgcalls.start
