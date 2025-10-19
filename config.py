import os
from dotenv import load_dotenv

load_dotenv()

# Настройка для поиска по ссылке на видео
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'quiet': False,
    'ignoreerrors': True, 
    'nocheckcertificate': True,
    'cachedir': False,
    'source_address': '0.0.0.0',
    'extractor_args': {
        'youtube': {
            'player_client': ['android','web']
            }
        },
}

# Настройка для поиска по названию видео
YDL_OPTIONS_FROM_TITLE = {
    'format': 'bestaudio/best',
    'extract_flat': True,
    'quiet': False,
    'ignoreerrors': True, 
    'nocheckcertificate': True,
    'cachedir': False,
    'noplaylist': True, 
    'default_search': 'ytsearch',
    'extractor_args': {
        'youtube': {
            'player_client': ['android','web']
            }
        },
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Промт для версии с AI(можно изменить под себя)
BASE_PROMPT = 'Ты - умный помощник. Отвечай на русском, по делу и дружелюбно\n'