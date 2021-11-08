import os
import re
import aiofiles
import yt_dlp
import aiohttp
import random
import asyncio
import shutil
import requests
from os import path
import time as sedtime
from time import time
from .. import converter
from asyncio import QueueEmpty
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from pytgcalls import StreamType
from Yukki.config import LOG_GROUP_ID
from youtubesearchpython import VideosSearch
from ..YukkiUtilities.tgcallsrun import ASS_ACC
from Yukki import app, BOT_USERNAME, dbb, SUDOERS
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from aiohttp import ClientResponseError, ServerTimeoutError, TooManyRedirects
from Yukki import dbb, app, BOT_USERNAME, BOT_ID, ASSID, ASSNAME, ASSUSERNAME, ASSMENTION
from Yukki.YukkiUtilities.tgcallsrun import (yukki, convert, download, clear, get, is_empty, put, task_done, smexy)
from ..YukkiUtilities.tgcallsrun import (yukki, convert, download, clear, get, is_empty, put, task_done)
from Yukki.YukkiUtilities.helpers.decorators import errors
from Yukki.YukkiUtilities.helpers.filters import command, other_filters
from Yukki.YukkiUtilities.helpers.paste import paste
from Yukki.YukkiUtilities.tgcallsrun import (yukki, clear, get, is_empty, put, task_done)
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.database.playlist import (get_playlist_count, _get_playlists, get_note_names, get_playlist, save_playlist, delete_playlist)
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from Yukki.YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup, audio_markup)
from Yukki.YukkiUtilities.helpers.inline import play_keyboard, confirm_keyboard, play_list_keyboard, close_keyboard, confirm_group_keyboard
from Yukki.YukkiUtilities.tgcallsrun import (yukki, convert, download, clear, get, is_empty, put, task_done, smexy)
from Yukki.YukkiUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Yukki.YukkiUtilities.database.onoff import (is_on_off, add_on, add_off)
from Yukki.YukkiUtilities.database.blacklistchat import (blacklisted_chats, blacklist_chat, whitelist_chat)
from Yukki.YukkiUtilities.database.gbanned import (get_gbans_count, is_gbanned_user, add_gban_user, add_gban_user)
from Yukki.YukkiUtilities.database.theme import (_get_theme, get_theme, save_theme)
from Yukki.YukkiUtilities.database.assistant import (_get_assistant, get_assistant, save_assistant)
from ..config import DURATION_LIMIT, ASS_ID
from ..YukkiUtilities.helpers.decorators import errors
from ..YukkiUtilities.helpers.filters import command
from ..YukkiUtilities.helpers.gets import (get_url, themes, random_assistant, ass_det)
from ..YukkiUtilities.helpers.thumbnails import gen_thumb
from ..YukkiUtilities.helpers.chattitle import CHAT_TITLE
from ..YukkiUtilities.helpers.ytdl import ytdl_opts 
from ..YukkiUtilities.helpers.inline import (play_keyboard, search_markup, play_markup, playlist_markup)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from pykeyboard import InlineKeyboard
from Yukki import aiohttpsession as session

pattern = re.compile(
    r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$"
)

flex = {}

async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False

    
@Client.on_callback_query(filters.regex(pattern=r"ppcl"))
async def closesmex(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        smex, user_id = callback_request.split("|") 
    except Exception as e:
        await CallbackQuery.message.edit(f"❌ an error occured\n\n**reason:** {e}")
        return 
    if CallbackQuery.from_user.id != int(user_id):
        await CallbackQuery.answer("💡 sorry this is not for you !", show_alert=True)
        return
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()
    
    
@Client.on_callback_query(filters.regex("pausevc"))
async def pausevc(_,CallbackQuery):
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await yukki.pytgcalls.pause_stream(chat_id)
            await music_off(chat_id)
            await CallbackQuery.answer("⏸ music playback has paused", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await CallbackQuery.message.reply(f"⏸ music playback has paused", reply_markup=play_keyboard)
            await CallbackQuery.message.delete()
        else:
            await CallbackQuery.answer(f"❌ no music is currently playing", show_alert=True)
            return
    else:
        await CallbackQuery.answer(f"❌ no music is currently playing", show_alert=True)
   
    
@Client.on_callback_query(filters.regex("resumevc"))
async def resumevc(_,CallbackQuery):  
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        if await is_music_playing(chat_id):
            await CallbackQuery.answer("❌ no music is paused", show_alert=True)
            return    
        else:
            await music_on(chat_id)
            await yukki.pytgcalls.resume_stream(chat_id)
            await CallbackQuery.answer("video chat resumed", show_alert=True)
            user_id = CallbackQuery.from_user.id
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await CallbackQuery.message.reply(f"▶ music playback has resumed", reply_markup=play_keyboard)
            await CallbackQuery.message.delete()
    else:
        await CallbackQuery.answer(f"❌ no music is currently playing", show_alert=True)
   
    
@Client.on_callback_query(filters.regex("skipvc"))
async def skipvc(_,CallbackQuery): 
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    chat_title = CallbackQuery.message.chat.title
    if await is_active_chat(chat_id):
        task_done(CallbackQuery.message.chat.id)
        if is_empty(CallbackQuery.message.chat.id):
            user_id = CallbackQuery.from_user.id
            await remove_active_chat(chat_id) 
            user_name = CallbackQuery.from_user.first_name
            rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
            await remove_active_chat(chat_id)
            await CallbackQuery.answer()
            await CallbackQuery.message.reply(f"**{rpk} want to skipped music**\n\n❌ no more music in __Queues__\n\n» userbot leaving voice chat")
            await yukki.pytgcalls.leave_group_call(chat_id)
            return
        else:
            await CallbackQuery.answer("💡 you've skipped to the next song", show_alert=True)
            afk = get(chat_id)['file']
            f1 = (afk[0])
            f2 = (afk[1])
            f3 = (afk[2])
            finxx = (f"{f1}{f2}{f3}")
            if str(finxx) != "raw":   
                mystic = await CallbackQuery.message.reply("💡 bot is currently playing playlist...\n\n📥 downloading next music from playlist...")
                url = (f"https://www.youtube.com/watch?v={afk}")
                try:
                    with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                        x = ytdl.extract_info(url, download=False)
                except Exception as e:
                    return await mystic.edit(f"failed to download this video.\n\n**reason:** {e}") 
                title = (x["title"])
                videoid = afk
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
                            sedtime.sleep(1)
                            mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                        if per > 500:    
                            if flex[str(bytesx)] == 2:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per > 800:    
                            if flex[str(bytesx)] == 3:
                                flex[str(bytesx)] += 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                        if per == 1000:    
                            if flex[str(bytesx)] == 4:
                                flex[str(bytesx)] = 1
                                sedtime.sleep(0.5)
                                mystic.edit(f"Downloading {title[:50]}.....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec") 
                                print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} in {chat_title} | ETA: {eta} seconds")
                loop = asyncio.get_event_loop()
                xx = await loop.run_in_executor(None, download, url, my_hook)
                file = await convert(xx)
                await yukki.pytgcalls.change_stream(
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
                ctitle = (await app.get_chat(chat_id)).title
                ctitle = await CHAT_TITLE(ctitle)
                f2 = open(f'search/{afk}id.txt', 'r')        
                userid =(f2.read())
                thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                user_id = userid
                buttons = play_markup(videoid, user_id)
                await mystic.delete()
                semx = await app.get_users(userid)
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
                await CallbackQuery.message.reply_photo(
                photo= thumb,
                reply_markup=InlineKeyboardMarkup(buttons),    
                caption=(f"⏭ <b>Skipped to the next music</b>\n\n🏷 <b>Name:</b> {title[:60]}\n⏱ <b>Duration:</b> `{duration} m`\n💡 **Status:** `Playing`\n🎧 **Request by:** {semx.mention}")
            )   
                os.remove(thumb)
            else:      
                await yukki.pytgcalls.change_stream(
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
                user_id = CallbackQuery.from_user.id
                user_name = CallbackQuery.from_user.first_name
                rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"    
                await CallbackQuery.message.reply_photo(
                photo=f"downloads/{_chat_}final.png",
                reply_markup=InlineKeyboardMarkup(buttons),
                caption=f"⏭ <b>Skipped to the next music</b>\n\n🏷 <b>Name:</b> {title[:60]}\n⏱ <b>Duration:</b> `{duration} m`\n💡 **Status:** `Playing`\n🎧 **Request by:** {username}",
                )
                return           
            
       
@Client.on_callback_query(filters.regex("stopvc"))
async def stopvc(_,CallbackQuery):
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    checking = CallbackQuery.from_user.first_name
    chat_id = CallbackQuery.message.chat.id
    if await is_active_chat(chat_id):
        try:
            clear(chat_id)
        except QueueEmpty:
            pass
        try:
            await yukki.pytgcalls.leave_group_call(chat_id)
        except Exception as e:
            pass
        await remove_active_chat(CallbackQuery.message.chat.id) 
        await CallbackQuery.answer("✅ music playback has ended", show_alert=True)
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"
        await CallbackQuery.edit_message_text("✅ this music playback has ended", reply_markup=close_keyboard)
    else:
        await CallbackQuery.answer(f"❌ no music is currently playing", show_alert=True)


@Client.on_callback_query(filters.regex("play_playlist"))
async def play_playlist(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        user_id,smex = callback_request.split("|") 
    except Exception as e:
        await CallbackQuery.answer()
        return await CallbackQuery.message.edit(f"an error occured\n**reason**: {e}")
    Name = CallbackQuery.from_user.first_name
    chat_title = CallbackQuery.message.chat.title
    if str(smex) == "personal":
        if CallbackQuery.from_user.id != int(user_id):
            return await CallbackQuery.answer("💡 this is not for you, play your own playlist", show_alert=True)
        _playlist = await get_note_names(CallbackQuery.from_user.id)
        if not _playlist:
            return await CallbackQuery.answer(f"❌ you have no playlist on server", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""💡 starting playlist

Group : {chat_title}
Req By : {Name}

▶ personal playlist playing."""
            mystic = await CallbackQuery.message.reply_text(f"💡 starting {Name}'s personal playlist.\n\n🎧 request by: {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"Queued Playlist:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.from_user.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"Queued Position: {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"failed to download this video.\n\n**reason:** {e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
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
                                try:
                                    if eta > 2:
                                        mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**Downloaded {title[:50]}.....**\n\n**FileSize:** {size}\n**Time Taken:** {taken} sec\n\n**Converting File** [__FFmpeg processing__]")
                            print(f"[{videoid}] Downloaded | Elapsed: {taken} seconds")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await yukki.pytgcalls.join_group_call(
                        chat_id,
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)  
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🏷 <b>Name:</b> [{title[:60]}]({url})\n⏱ <b>Duration:</b> {duration}\n💡 **Status:** `Playing`\n🎧 <b>Request by:</b> {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("🔄 pasting queued playlist to bin...")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"Checkout Queued Playlist", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▶️", callback_data=f'resumevc2'),
                    InlineKeyboardButton(text="⏸️", callback_data=f'pausevc2'),
                    InlineKeyboardButton(text="⏭️", callback_data=f'skipvc2'),
                    InlineKeyboardButton(text="⏹️", callback_data=f'stopvc2')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="🗑 Close", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"This is queued personal playlist of {Name}.\n\nIf you want to delete any music from playlist use: /delmyplaylist", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()
    if str(smex) == "group":
        _playlist = await get_note_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.answer(f"This Group not have a playlist on database, try to adding music into playlist.", show_alert=True)
        else:
            await CallbackQuery.message.delete()
            logger_text=f"""💡 starting playlist

Group : {chat_title}
Req By : {Name}

▶ Group's playlist playing."""
            mystic = await CallbackQuery.message.reply_text(f"💡 starting Groups's playlist.\n\n🎧 request By: {CallbackQuery.from_user.first_name}")   
            checking = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
            msg = f"Queued Playlist:\n\n"
            j = 0
            for note in _playlist:
                _note = await get_playlist(CallbackQuery.message.chat.id, note)
                title = _note["title"]
                videoid = _note["videoid"]
                url = (f"https://www.youtube.com/watch?v={videoid}")
                duration = _note["duration"]
                if await is_active_chat(chat_id):
                    position = await put(chat_id, file=videoid)
                    j += 1
                    msg += f"{j}- {title[:50]}\n"
                    msg += f"Queued Position: {position}\n\n"
                    f20 = open(f'search/{videoid}id.txt', 'w')
                    f20.write(f"{user_id}") 
                    f20.close()
                else:
                    try:
                        with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                            x = ytdl.extract_info(url, download=False)
                    except Exception as e:
                        return await mystic.edit(f"failed to download this video.\n\n**reason:** {e}") 
                    title = (x["title"])
                    thumbnail = (x["thumbnail"])
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
                                try:
                                    if eta > 2:
                                        mystic.edit(f"Downloading {title[:50]}\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                except Exception as e:
                                    pass
                            if per > 250:    
                                if flex[str(bytesx)] == 2:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}..\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 500:    
                                if flex[str(bytesx)] == 3:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:     
                                        mystic.edit(f"Downloading {title[:50]}...\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                            if per > 800:    
                                if flex[str(bytesx)] == 4:
                                    flex[str(bytesx)] += 1
                                    if eta > 2:    
                                        mystic.edit(f"Downloading {title[:50]}....\n\n**FileSize:** {size}\n**Downloaded:** {percentage}\n**Speed:** {speed}\n**ETA:** {eta} sec")
                                    print(f"[{videoid}] Downloaded {percentage} at a speed of {speed} | ETA: {eta} seconds")
                        if d['status'] == 'finished': 
                            try:
                                taken = d['_elapsed_str']
                            except Exception as e:
                                taken = "00:00"
                            size = d['_total_bytes_str']
                            mystic.edit(f"**Downloaded: {title[:50]}...**\n\n**Size:** {size}\n**Time:** `{taken}` sec\n\n**Converting File** [__FFmpeg processing__]")
                            print(f"[{videoid}] Downloaded | Elapsed: {taken} seconds")  
                    loop = asyncio.get_event_loop()
                    xx = await loop.run_in_executor(None, download, url, my_hook)
                    file = await convert(xx)
                    await music_on(chat_id)
                    await add_active_chat(chat_id)
                    await yukki.pytgcalls.join_group_call(
                        chat_id,
                        InputStream(
                            InputAudioStream(
                                file,
                            ),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    theme = random.choice(themes)
                    ctitle = CallbackQuery.message.chat.title
                    ctitle = await CHAT_TITLE(ctitle)
                    thumb = await gen_thumb(thumbnail, title, userid, theme, ctitle)
                    buttons = play_markup(videoid, user_id)
                    m = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),    
                    caption=(f"🏷 <b>Name:</b> [{title[:60]}]({url})\n⏱ <b>Duration:</b> `{duration}` m\n💡 **Status:** `Playing`\n🎧 <b>Request by:</b> {checking}")
                )   
                    os.remove(thumb)
                    await CallbackQuery.message.delete()
        await asyncio.sleep(1)
        await mystic.delete()
        m = await CallbackQuery.message.reply_text("🔄 pasting queued playlist to bin...")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        a1 = InlineKeyboardButton(text=f"Checkout Queued Playlist", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="▶️", callback_data=f'resumevc2'),
                    InlineKeyboardButton(text="⏸️", callback_data=f'pausevc2'),
                    InlineKeyboardButton(text="⏭️", callback_data=f'skipvc2'),
                    InlineKeyboardButton(text="⏹️", callback_data=f'stopvc2')
                ],
                [
                    a1,
                ],
                [
                    InlineKeyboardButton(text="🗑 Close", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, caption=f"This is queued playlist of this Group.\n\nIf you want to delete any music from playlist use: /delchatplaylist", quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_text(
                    text=msg, reply_markup=key
                )
            await m.delete()


@Client.on_callback_query(filters.regex("group_playlist"))
async def group_playlist(_,CallbackQuery):
    await CallbackQuery.answer()
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"❌ an error occured\n\n**reason:** {e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(chat_id)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("💡 Generating Group's playlist in database...")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        return await CallbackQuery.message.reply_text("💡 sorry, you can only have 30 music in group's playlist.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"❌ an error occured.\n\nplease forward to @VeezSupportGroup\n\n**reason:** {e}") 
    _check = await get_playlist(chat_id, videoid)
    title = title[:50]
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, your request is already **added** to the **playlist !**")   
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(chat_id, videoid, assis)
    Name = CallbackQuery.from_user.first_name
    return await CallbackQuery.message.reply_text(f"✅ added to **Group's playlist**\n\n👤 **By :** {Name}")
  

@Client.on_callback_query(filters.regex("playlist"))
async def pla_playylistt(_,CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    chat_id = CallbackQuery.message.chat.id
    callback_request = callback_data.split(None, 1)[1]
    userid = CallbackQuery.from_user.id 
    try:
        url,smex= callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"❌ an error occured\n\n**reason:** {e}")
    Name = CallbackQuery.from_user.first_name
    _count = await get_note_names(userid)
    count = 0
    if not _count:
        sex = await CallbackQuery.message.reply_text("💡 Generating your personal playlist in database...")
        await asyncio.sleep(2)
        await sex.delete()
    else:
        for smex in _count:
            count += 1   
    count = int(count)
    if count == 30:
        if userid in SUDOERS:
            pass
        else:
            return await CallbackQuery.message.reply_text("💡 sorry, you can only have 30 music in your playlist.")
    try:
        url = (f"https://www.youtube.com/watch?v={url}")
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
            duration = (result["duration"])
            videoid = (result["id"])
    except Exception as e:
            return await CallbackQuery.message.reply_text(f"an error occured.\n\nplease forward to @VeezSupportGroup\n**Possible Reason:**{e}") 
    _check = await get_playlist(userid, videoid)
    if _check:
         return await CallbackQuery.message.reply_text(f"{Name}, your request is **already added** to the **playlist !**") 
    title = title[:50]    
    assis = {
        "videoid": videoid,
        "title": title,
        "duration": duration,
    }
    await save_playlist(userid, videoid, assis)
    return await CallbackQuery.message.reply_text(f"✅ added to **personal playlist**\n\n👤 **for :** {Name}")   
    

@Client.on_callback_query(filters.regex("P_list"))
async def P_list(_,CallbackQuery):
    _playlist = await get_note_names(CallbackQuery.from_user.id)
    if not _playlist:
        return await CallbackQuery.answer(f"❌ you not have personal playlist on database, try to adding music in playlist.", show_alert=True)
    else:
        j = 0
        await CallbackQuery.answer()
        msg = f"Personal Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.from_user.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"Duration: {duration} min(s)\n\n"   
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()     
        m = await CallbackQuery.message.reply_text("🔄 pasting playlist to bin...")
        link = await paste(msg)
        preview = link + "/preview.png"
        print(link)
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a2 = InlineKeyboardButton(text=f"💡 play {user_name[:17]}'s playlist", callback_data=f'play_playlist {user_id}|personal')
        a3 = InlineKeyboardButton(text=f"🔗 Check Playlist", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a2,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="🗑 Close", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception as e :
                print(e)
                pass
        else:
            print("5")
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
    
    
@Client.on_callback_query(filters.regex("G_list"))
async def G_list(_,CallbackQuery):
    user_id = CallbackQuery.from_user.id
    _playlist = await get_note_names(CallbackQuery.message.chat.id)
    if not _playlist:
        return await CallbackQuery.answer(f"❌ you not have Group playlist on database, try to adding music in playlist.", show_alert=True)
    else:
        await CallbackQuery.answer()
        j = 0
        msg = f"Group Playlist:\n\n"
        for note in _playlist:
            j += 1
            _note = await get_playlist(CallbackQuery.message.chat.id, note)
            title = _note["title"]
            duration = _note["duration"]
            msg += f"{j}- {title[:60]}\n"
            msg += f"    Duration- {duration} Min(s)\n\n"
        await CallbackQuery.answer()
        await CallbackQuery.message.delete()
        m = await CallbackQuery.message.reply_text("🔄 pasting playlist to bin...")
        link = await paste(msg)
        preview = link + "/preview.png"
        urlxp = link + "/index.txt"
        user_id = CallbackQuery.from_user.id
        user_name = CallbackQuery.from_user.first_name
        a1 = InlineKeyboardButton(text=f"💡 play Group's playlist", callback_data=f'play_playlist {user_id}|group')
        a3 = InlineKeyboardButton(text=f"🔗 Check Playlist", url=urlxp)
        key = InlineKeyboardMarkup(
            [
                [
                    a1,
                ],
                [
                    a3,
                    InlineKeyboardButton(text="🗑 Close", callback_data=f'close2')
                ]    
            ]
        )
        if await isPreviewUp(preview):
            try:
                await CallbackQuery.message.reply_photo(
                    photo=preview, quote=False, reply_markup=key
                )
                await m.delete()
            except Exception:
                pass
        else:
            await CallbackQuery.message.reply_photo(
                    photo=link, quote=False, reply_markup=key
                )
            await m.delete()
                       
        
@Client.on_callback_query(filters.regex("cbgroupdel"))
async def cbgroupdel(_,CallbackQuery):  
    a = await app.get_chat_member(CallbackQuery.message.chat.id , CallbackQuery.from_user.id)
    if not a.can_manage_voice_chats:
        return await CallbackQuery.answer("you must be admin with permissions:\n\n❌ » Manage video chat", show_alert=True)
    await CallbackQuery.message.delete() 
    await CallbackQuery.answer()
    _playlist = await get_note_names(CallbackQuery.message.chat.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("💡 Group not have a playlist on veez music mega database.")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.message.chat.id, note)
    await CallbackQuery.message.reply_text("✅ successfully deleted your Group's whole playlist")  
    
    
@Client.on_callback_query(filters.regex("cbdel"))
async def delplcb(_,CallbackQuery): 
    await CallbackQuery.answer()
    await CallbackQuery.message.delete() 
    _playlist = await get_note_names(CallbackQuery.from_user.id)                                    
    if not _playlist:
        return await CallbackQuery.message.reply_text("💡 you not have a playlist on veez music mega database.")
    else:
        titlex = []
        for note in _playlist:
            await delete_playlist(CallbackQuery.from_user.id, note)
    await CallbackQuery.message.reply_text("✅ successfully deleted your whole playlist")
