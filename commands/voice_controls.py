from discord.ext import commands

@commands.command()
async def join(ctx):
    """Подключает бота к голосовому каналу"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Подключился к каналу {channel}")
    else:
        await ctx.send("Вы должны быть в голосовом канале!")

@commands.command()
async def leave(ctx):
    """Отключает бота из голосового канала"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Бот не в голосовом канале!")