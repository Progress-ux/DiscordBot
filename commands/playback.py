from discord.ext import commands
from commands.music import play_next
from config import FFMPEG_OPTIONS
import discord
import asyncio


@commands.command()
async def skip(ctx):
    """Пропускает текущий трек и воспроизводит следующий"""

    if ctx.voice_client and ctx.voice_client.is_playing():
        if ctx.bot.state.isRepeat:
            await repeat(ctx)
        ctx.voice_client.stop()
        ctx.state.should_play_next = False  
        await ctx.send("⏭ Пропущен текущий трек.")
        await play_next(ctx)
    else:
        await ctx.send("Сейчас ничего не играет!")


@commands.command()
async def back(ctx):
    """Возвращает на предыдущий трек"""

    title, url = ctx.bot.state.backTrack()
    if not title or not url:
        await ctx.send("❌ Нет предыдущих треков!")
    else:
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                if ctx.bot.state.isRepeat:
                    await repeat(ctx)
                ctx.voice_client.stop()
                ctx.bot.state.should_play_next = False

                await ctx.send(f"⏮ Возвращаюсь к предыдущему треку: {title}")
                source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), ctx.bot.loop))
        except Exception as e:
            await ctx.send(f"❌ Ошибка загрузки: {e}")


@commands.command()
async def repeat(ctx):
    """Включение/выключение автоповтора"""

    ctx.bot.state.isRepeat = not ctx.bot.state.isRepeat
    status = "включен 🔁" if ctx.bot.state.isRepeat else "выключен ❌"
    await ctx.send(f"🔁 Автоповтор {status}")


@commands.command()
async def pause(ctx):
    """Ставит музыку на паузу"""

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸ Музыка на паузе")
    else:
        await ctx.send("Сейчас ничего не играет!")


@commands.command()
async def resume(ctx):
    """Возобновляет воспроизведение"""

    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶ Музыка продолжается")
    else:
        await ctx.send("Музыка не на паузе!")


@commands.command()
async def stop(ctx):
    """Останавливает музыку"""

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        ctx.bot.state.should_play_next = False
        await ctx.send("⏹ Музыка остановлена")
    else:
        await ctx.send("Сейчас ничего не играет!")


@commands.command()
async def clear(ctx):
    """Очищает очередь"""
    ctx.bot.state.clearAll()
    await ctx.send("🗑 Очередь очищена.")