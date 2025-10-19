import yt_dlp
import asyncio
import re
from config import YDL_OPTIONS, YDL_OPTIONS_FROM_TITLE

# Проверка ссылки и очистка
def clean_url(url):
    if 'playlist' not in url and 'list=' in url:
        return re.sub(r"(\?list=[^&]+)", "", url)
    return url

# Проверка на ссылку 
def is_url(string):
    return re.match(r'^https?://', string) is not None


# Нужен для обработки плейлистов
async def extract_info(url):
    return await asyncio.to_thread(lambda: yt_dlp.YoutubeDL(YDL_OPTIONS).extract_info(url, download=False, process=False))

# Поиск видео по названию
async def extract_info_search(query):
    def search():
        with yt_dlp.YoutubeDL(YDL_OPTIONS_FROM_TITLE) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            return info['entries'][0]
    return await asyncio.to_thread(search)

# Получение ссылки на аудио 
async def download_audio(url):
    def get_audio():
        with yt_dlp.YoutubeDL({
            'format': 'bestaudio/best',
            'quiet': True,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'cachedir': False
        }) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                return None
            # Если это плейлист, берем первый элемент
            if 'entries' in info:
                for entry in info['entries']:
                    if entry is not None and entry.get('url'):
                        return entry['url']
                return None
            return info.get('url')
    return await asyncio.to_thread(get_audio)

# Асинхронная загрузка оставшихся треков плейлиста
async def load_rest(info, ctx):
    entries = list(info.get('entries', []))  
    if len(entries) <= 1:
        await ctx.send("🎶 Плейлист загружен: 0 треков.")
        return

    async def process_entry(entry):
        if entry is None:
            return
        entry_url = entry.get('url')
        if not entry_url:
            return

        def extract():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                return ydl.extract_info(entry_url, download=False)

        result = await asyncio.to_thread(extract)
        if result is None:
            return
        track_url = result.get('url')
        if not track_url:
            return

        track_title = entry.get('title', 'Неизвестный трек')
        ctx.bot.state.addTrack(track_title, track_url)

    # Пропускаем первый трек, который уже играет
    tasks = [process_entry(e) for e in entries[1:]]
    await asyncio.gather(*tasks)
    await ctx.send(f"🎶 Плейлист загружен: {len(tasks)} треков.")
