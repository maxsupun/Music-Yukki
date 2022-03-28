from Yukki import app
from ..YukkiUtilities.helpers.decorators import errors
from ..YukkiUtilities.helpers.filters import command, other_filters
from Yukki.YukkiUtilities.database.playlist import get_note_names, get_playlist, delete_playlist
from Yukki.YukkiUtilities.helpers.inline import confirm_keyboard, play_list_keyboard, confirm_group_keyboard

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "all","16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]   


@Client.on_message(command(["playlist", "playlist@VeezMegaBot"]) & other_filters)
async def start_playlist_cmd(_, message):
    thumb ="cache/playlist.png"
    await message.reply_photo(
    photo=thumb, 
    caption=("**❓ Which playlist do you want to play?**"),    
    reply_markup=play_list_keyboard) 
    return 


@Client.on_message(command(["delmyplaylist", "delmyplaylist@VeezMegaBot"]) & other_filters)
async def del_personal_playlist(_, message):
    usage = ("usage:\n\n/delmyplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delmyplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 18:
        return await message.reply_text(f"💡 **Confirmation** !\n\nThe playlist will be lost, are you sure want to delete your whole personal playlist ?", reply_markup=confirm_keyboard)
    else:
         _playlist = await get_note_names(message.from_user.id)
    if not _playlist:
        await message.reply_text("You not have playlist on database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.from_user.id, note)
            if j == count:
                deleted = await delete_playlist(message.from_user.id, note)
                if deleted:
                    return await message.reply_text(f"✅ Deleted the {count} music in personal playlist")
                else:
                    return await message.reply_text("no such saved music in your playlist !")                                
        await message.reply_text("You not have such music in personal playlist !")                             


@Client.on_message(command(["delchatplaylist", "delchatplaylist@VeezMegaBot"]) & other_filters)
async def del_chat_playlist(_, message):
    a = await app.get_chat_member(message.chat.id , message.from_user.id)
    if not a.can_manage_voice_chats:
        return await message.reply_text("You're missing admin rights to use this command.\n\n» ❌ can_manage_voice_chats")
    usage = ("usage:\n\n/delchatplaylist [numbers between 1-30] (to delete a particular music in playlist)\n\n/delchatplaylist all (to delete whole playlist)")
    if len(message.command) < 2:
        return await message.reply_text(usage)
    name = message.text.split(None, 1)[1].strip()
    if not name:
        return await message.reply_text(usage)
    if name not in options:
        return await message.reply_text(usage)
    if len(message.text) == 20:
        return await message.reply_text(f"💡 Confirmation !\n\nThe playlist will be lost, are you sure want to delete the whole Group playlist ?", reply_markup=confirm_group_keyboard)
    else:
         _playlist = await get_note_names(message.chat.id)
    if not _playlist:
        await message.reply_text("Group's has no playlist on database !")
    else:
        titlex = []
        j = 0
        count = int(name)
        for note in _playlist:
            j += 1
            _note = await get_playlist(message.chat.id, note)
            if j == count:
                deleted = await delete_playlist(message.chat.id, note)
                if deleted:
                    return await message.reply_text(f"✅ Deleted the {count} music in group's playlist")
                else:
                    return await message.reply_text("no such saved music in group playlist !")                                
        await message.reply_text("This chat not have such music in Group's playlist !")
