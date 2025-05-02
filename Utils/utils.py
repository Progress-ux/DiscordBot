import yt_dlp
import asyncio
import re
from config import YDL_OPTIONS
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor()

def clean_url(url):
    if 'playlist' not in url and 'list=' in url:
        cleaned_url = re.sub(r"(\?list=[^&]+)", "", url)
        return cleaned_url
    else:
        return url

def extract_info(url):
    with yt_dlp.YoutubeDL({
        'format': 'bestaudio/best',
        'extract_flat': True,
        'quiet': True,
        'ignoreerrors': True
    }) as ydl:
        return ydl.extract_info(url, download=False, process=False)

def download_audio(url):
    with yt_dlp.YoutubeDL({
        'format': 'bestaudio/best',
        'extract_flat': True,
        'quiet': True,
        'ignoreerrors': True
    }) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']  
    
async def load_rest(info, ctx):

    loop = asyncio.get_running_loop()
    i = 0

    def extract(entry_url):
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            return ydl.extract_info(entry_url, download=False)

    for entry in info['entries']:
        if entry is None or i == 0:
            i += 1
            continue
        try:
            entry_url = entry.get('url')
            if not entry_url:
                continue

            result = await loop.run_in_executor(executor, extract, entry_url)
            track_title = entry.get('title', 'Неизвестный трек')
            track_audio_url = result['url']
            ctx.bot.state.addTrack(track_title, track_audio_url)
            i += 1
        except Exception as ex:
            print(f"[ERROR] Пропущен трек из-за ошибки: {ex}")

    await ctx.send(f"🎶 Плейлист загружен: {i} треков.")

