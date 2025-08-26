import discord
import asyncio
from discord.ext import commands

# Импорт токена и плеера
from config import DISCORD_TOKEN
from player_state import PlayerState

# Импорт команд
from commands.music import play
from commands.playback import skip, back, repeat, repeatP, pause, resume, stop, clear
from commands.playlist import playlist, history
from commands.voice_controls import join, leave
from commands.ping import ping
from commands.help import help_command
from commands.ask import ask

# Настройка интентов
intents = discord.Intents.default()
intents.message_content = True

# Инициализация бота
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
bot.state = PlayerState()

@bot.event
async def on_ready():
    print(f'✅ Бот запущен как {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        if before.channel and not after.channel:
            bot.state.clear()
        elif not before.channel and after.channel:
            bot.state.clear()


# Регистрация команд
command_list = [
    play, skip, back, repeat, repeatP, pause, resume, 
    stop, clear, playlist, history, join, 
    leave, help_command, ask, ping
]

for cmd in command_list:
    bot.add_command(cmd)

# Старт бота
async def run_bot():
    await bot.start(DISCORD_TOKEN)

asyncio.run(run_bot())
