from yt_dlp import YoutubeDL

ytdl = YoutubeDL(
    {
        "format": "bestaudio[ext=m4a]",
        "geo_bypass": True,
        "noprogress": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "no_warnings": True,
        "quite": True,
    }
)

ytdl_opts = {"format": "bestaudio[ext=m4a]", "quiet": True}
