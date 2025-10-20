import yt_dlp
import asyncio
import re
from config import YDL_OPTIONS, YDL_OPTIONS_FROM_TITLE, YDL_OPTIONS_FROM_PLAYLIST

# Проверка ссылки и очистка
def clean_url(url):
    if 'playlist' not in url and 'list=' in url:
        return re.sub(r"(\?list=[^&]+)", "", url)
    return url

# Проверка на ссылку 
def is_url(string):
    return re.match(r'^https?://', string) is not None

def extract_playlist_ids(url):
    with yt_dlp.YoutubeDL(YDL_OPTIONS_FROM_PLAYLIST) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info or 'entries' not in info:
            return []
        # Извлекаем ID всех видео
        ids = ["https://youtu.be/" + entry['id'] for entry in info['entries'] if entry]
        return ids

def extract_info(url):
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        return ydl.extract_info(url, download=False)

async def add_track(ctx, url):
    try:
        info = await asyncio.to_thread(extract_info, url)

        track_title = info.get('title', 'Неизвестный трек')
        track_audio_url = await download_audio(url)

        ctx.bot.state.addTrack(track_title, track_audio_url)
        return track_title
    
    except Exception as e:
        print(e)

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

# Асинхронная загрузка треков из плейлиста
async def load_playlist(ctx, playlist_url):
    await ctx.send(f"🎶 Найдено {len(playlist_url)} треков в плейлисте. Загружаю...")

    # Пропускаем первый трек, если он уже играет
    for i, video_url in enumerate(playlist_url[1:], start=2):
        try:
            def extract():
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    return ydl.extract_info(video_url, download=False)
            info = await asyncio.to_thread(extract)
            if info is None:
                continue
            track_url = info.get('url')
            track_title = info.get('title', 'Неизвестный трек')

            if track_url:
                ctx.bot.state.addTrack(track_title, track_url)
        except Exception:
            continue

    await ctx.send(f"✅ Плейлист загружен: {len(playlist_url) - 1} треков добавлено.")