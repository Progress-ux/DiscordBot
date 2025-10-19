from discord.ext import commands
from commands.voice_controls import join
from Utils.utils import clean_url, extract_info_search, download_audio, is_url, extract_playlist_ids, load_playlist, extract_first
import asyncio
from config import FFMPEG_OPTIONS
import discord

@commands.command()
async def play(ctx, *, query: str):
    """Добавить трек в очередь и начать воспроизведение"""

    if not ctx.voice_client:
        await ctx.invoke(join)
    
    try:
        # Обработка ссылки
        if is_url(query):
            cleanurl = clean_url(query)
        else:
            info = await extract_info_search(query)
            cleanurl = info['url']

        if 'playlist' in cleanurl:
            await ctx.send("🎵 Начинаю загрузку плейлиста!")
            playlist_urls = extract_playlist_ids(cleanurl)

            if not playlist_urls:
                await ctx.send("❌ Не удалось загрузить плейлист.")
                return

            first_url = playlist_urls[0]

            # Получаем информацию о первом треке
            first_info = await asyncio.to_thread(extract_first, first_url)

            if not first_info:
                await ctx.send("❌ Не удалось получить данные первого трека.")
                return

            first_title = first_info.get('title', 'Неизвестный трек')
            first_audio_url = await download_audio(first_url)

            ctx.bot.state.addTrack(first_title, first_audio_url)
            await ctx.send(f"🎵 Добавлен первый трек из плейлиста: {first_title}")

            # Если ничего не играет — запускаем воспроизведение
            if not ctx.voice_client.is_playing():
                await play_next(ctx)

            # Загружаем остальные треки асинхронно (в фоне)
            asyncio.create_task(load_playlist(ctx, cleanurl))
                
            

        # Загрузка одиночного трека в очередь
        else:
            track_title = info.get('title', 'Неизвестный трек')
            track_audio_url = await download_audio(cleanurl)
            ctx.bot.state.addTrack(track_title, track_audio_url)
            await ctx.send(f"🎵 Добавлен трек: {track_title}")
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
    except Exception as e:
        await ctx.send(f"❌ Ошибка загрузки: {e}")

# Функция для автоматического продолжения очереди
async def play_next(ctx):
    """Проигрывает следующий трек в очереди"""

    # Флаг для выключения треков
    if not ctx.bot.state.should_play_next or (not ctx.bot.state.track_queue and not ctx.bot.state.isRepeat):
        ctx.bot.state.should_play_next = True
        return
    
    # Загрузка следующего трека из очереди
    title, url = ctx.bot.state.popNextTrack()

    if ctx.bot.state.isRepeatPlaylist and title is None and url is None:
        ctx.bot.state.loopPlaylist()

    if title is None and url is None:
        await ctx.send("❌ Очередь пуста.")
        return

    try:
        await ctx.send(f"▶ Начинаю воспроизведение: {title}")
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop)) 
    except Exception as e:
        await ctx.send(f"❌ Ошибка загрузки: {e}")
