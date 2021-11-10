from yt_dlp import YoutubeDL

ytdl = YoutubeDL(
    {
        "format": "bestaudio[ext=m4a]",
        "geo-bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
    }
)

ytdl_opts = {"format" : "bestaudio[ext=m4a]", "quiet":True}
