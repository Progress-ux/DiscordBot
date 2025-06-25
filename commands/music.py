from discord.ext import commands
from commands.voice_controls import join
from Utils.utils import clean_url, extract_info, extract_info_search, download_audio, load_rest, is_url
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
            info = await extract_info(cleanurl)
        else:
            info = await extract_info_search(query)
            cleanurl = info['url']

        # Проверка на плейлист для более удобной загрузки в очередь
        if 'entries' in info:
            for entry in info['entries']:
                track_title = entry.get('title', 'Неизвестный трек')
                track_url = entry.get('url')
                track_audio_url = await download_audio(track_url)
                ctx.bot.state.addTrack(track_title, track_audio_url)
                await ctx.send(f"🎵 Добавлен трек: {track_title}")
                break

            if not ctx.voice_client.is_playing():
                await play_next(ctx)
            asyncio.create_task(load_rest(info, ctx))

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
    if title is None and url is None:
        await ctx.send("❌ Очередь пуста.")
        return

    try:
        await ctx.send(f"▶ Начинаю воспроизведение: {title}")
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop)) 
    except Exception as e:
        await ctx.send(f"❌ Ошибка загрузки: {e}")
