import os
import wget
import speedtest

from PIL import Image
from Yukki import app, SUDOERS
from Yukki.YukkiUtilities.database.onoff import is_on_off
from pyrogram import filters, Client
from pyrogram.types import Message


@app.on_message(filters.command("speedtest") & ~filters.edited)
async def run_speedtest(_, message):
    userid = message.from_user.id
    if await is_on_off(2):
        if userid in SUDOERS:
            pass
        else:
            return
    m = await message.reply_text("⚡️ running server speedtest")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("⚡️ running download speedtest")
        test.download()
        m = await m.edit("⚡️ running upload speedtest")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await m.edit_text(e)
        return 
    m = await m.edit_text("🔄 sharing speedtest results")
    path = wget.download(result["share"])
    try:
        img = Image.open(path)
        c = img.crop((17, 11, 727, 389))
        c.save(path)
    except Exception:
        pass
    output = f"""💡 **SpeedTest Results**
    
<u>**Client:**</u>

**ISP:** {result['client']['isp']}
**Country:** {result['client']['country']}
  
<u>**Server:**</u>

**Name:** {result['server']['name']}
**Country:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Latency:** {result['server']['latency']}  

⚡ **Ping:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
