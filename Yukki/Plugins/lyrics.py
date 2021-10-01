from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaDocument,
    InputMediaVideo,
    InputMediaAudio,
    Message,
)
from Yukki import app
from pyrogram import Client, filters
from youtubesearchpython import VideosSearch
import lyricsgenius
import re

@Client.on_callback_query(filters.regex(pattern=r"lyrics"))
async def lyricssex(_,CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    try:
        id, user_id = callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"Error Occured\n**Possible reason could be**:{e}")
    url = (f"https://www.youtube.com/watch?v={id}")
    print(url)
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = (result["title"])
    except Exception as e:
        return await CallbackQuery.answer("song not found, due to youtube issues.", show_alert=True)   
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    print(title)
    t = re.sub(r'[^\w]', ' ', title)
    print(t)
    y.verbose = False
    S = y.search_song(t, get_full_info=False)
    if S is None:
        return await CallbackQuery.answer("❌ lyrics not found", show_alert=True)
    await CallbackQuery.message.delete()
    userid = CallbackQuery.from_user.id
    usr = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    xxx = f"""
⚡️ __Powered by Veez Music AI__

**Searched By:-** {usr}
**Searched Song:-** __{title}__

**Lyrics Found:-** __{S.title}__
**Artist:-** {S.artist}

**__Lyrics:__**

{S.lyrics}"""
    await CallbackQuery.message.reply_text(xxx)
    
    
@Client.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):  
    m = await message.reply_text("searching lyrics...")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("❌ lyrics not found")
    xxx = f"""
⚡️ __Powered by Veez Music AI__

**Searched Song:-** __{query}__

**Lyrics Found:-** __{S.title}__
**Artist:-** {S.artist}

**__Lyrics:__**

{S.lyrics}"""
    await m.edit(xxx)
    
