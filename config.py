import os
from dotenv import load_dotenv

load_dotenv()

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'quiet': True,
    'ignoreerrors': True, 
    'nocheckcertificate': True,
    'cachedir': False
}

YDL_OPTIONS_FROM_TITLE = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'quiet': True,
    'ignoreerrors': True, 
    'nocheckcertificate': True,
    'cachedir': False,
    'noplaylist': True, 
    'default_search': 'ytsearch'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")