from discord.ext import commands

@commands.command()
async def playlist(ctx):
    """Показывает текущую очередь треков"""
    queue = ctx.bot.state.getQueueList()
    
    if not queue:
        await ctx.send("📭 Очередь пуста.")
        return

    track_list = ""
    for i, (title, _) in enumerate(queue, start=1):
        track_list += f"{i}. {title}\n"

    if len(track_list) > 1900:
        track_list = track_list[:1900] + "...\nСлишком много треков для показа!"
    
    await ctx.send(f"🎵 **Очередь треков:**\n{track_list}")


@commands.command()
async def history(ctx):
    """Показывает историю треков"""
    history = ctx.bot.state.getHistoryList()
    
    if not history:
        await ctx.send("📭 История пуста.")
        return

    track_list = ""
    for i, (title, _) in enumerate(history, start=1):
        track_list += f"{i}. {title}\n"

    if len(track_list) > 1900:
        track_list = track_list[:1900] + "...\nСлишком много треков для показа!"
    
    await ctx.send(f"🎶 **История треков:**\n{track_list}")
