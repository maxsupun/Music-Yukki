from os import path
import youtube_dl
from youtube_dl.utils import DownloadError

ytdl = youtube_dl.YoutubeDL(
    {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
    }
 )


def download(url: str, my_hook) -> str:       
    ydl_optssx = {
        'format' : 'bestaudio/best',
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        'quiet': True,
        'no_warnings': True,
    }
    info = ytdl.extract_info(url, False)
    try:
        x = youtube_dl.YoutubeDL(ydl_optssx)
        x.add_progress_hook(my_hook)
        dloader = x.download([url])
    except Exception as y_e:
        return print(y_e)
    else:
        dloader
    xyz = path.join("downloads", f"{info['id']}.{info['ext']}")
    return xyz
