from discord.ext import commands
from Utils.ask_ollama_util import ask_ollama, ollama_online, split_message

@commands.command()
async def ask(ctx, *, question):
    if not ollama_online():
        await ctx.send("Нейросеть сейчас недоступна")
        return
    
    await ctx.send("Думаю...")

    try:
        answer = ask_ollama(question)
        if not answer:
            await ctx.send("Ответ от нейросети пустой или непонятный")
            return
        # Проверка на кол-во символов (<2000) и разбиения на несколько сообщений
        for chunk in split_message(answer):
            await ctx.send(chunk)
    except Exception as e:
        await ctx.send(f"Error: {e}")
