import os
from dotenv import load_dotenv

load_dotenv()

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'quiet': False,
    'ignoreerrors': True, 
    'nocheckcertificate': True,
    'cachedir': False
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")