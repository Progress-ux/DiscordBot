import yt_dlp
import asyncio
import re
from config import YDL_OPTIONS, YDL_OPTIONS_FROM_TITLE
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor()

# Позволяет правильно обрабатывать ссылки на радио
def clean_url(url):
    if 'playlist' not in url and 'list=' in url:
        cleaned_url = re.sub(r"(\?list=[^&]+)", "", url)
        return cleaned_url
    else:
        return url

# Проверка на ссылку 
def is_url(string):
    return re.match(r'^https?://', string) is not None


# Нужен для обработки плейлистов
async def extract_info(url):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, lambda: yt_dlp.YoutubeDL(YDL_OPTIONS).extract_info(url, download=False, process=False))
    
async def extract_info_search(query):
    loop = asyncio.get_running_loop()
    def search():
        with yt_dlp.YoutubeDL(YDL_OPTIONS_FROM_TITLE) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            return info['entries'][0] 
    return await loop.run_in_executor(executor, search)

# Получает ссылку на аудио 
async def download_audio(url):
    loop = asyncio.get_running_loop()
    def get_audio():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']  
    return await loop.run_in_executor(executor, get_audio)

# Загрузка аудио-ссылок в отдельном потоке
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

