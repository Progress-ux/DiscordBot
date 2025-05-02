import discord
import asyncio
from discord.ext import commands
from config import DISCORD_TOKEN
from commands.music import play
from commands.playback import skip, back, repeat, pause, resume, stop, clear
from commands.playlist import playlist, history
from commands.voice_controls import join,leave
from player_state import PlayerState

intents = discord.Intents.default()
intents.message_content = True

player_state = PlayerState()
bot = commands.Bot(command_prefix="!", intents=intents)

bot.state = player_state

@bot.event
async def on_ready():
    print(f'✅ Бот запущен как {bot.user}')

# Регистрация команд
bot.add_command(play)

bot.add_command(skip)
bot.add_command(back)
bot.add_command(repeat)
bot.add_command(pause)
bot.add_command(resume)
bot.add_command(stop)
bot.add_command(clear)

bot.add_command(playlist)
bot.add_command(history)

bot.add_command(join)
bot.add_command(leave)

async def run_bot():
    await bot.start(DISCORD_TOKEN)

asyncio.run(run_bot())
