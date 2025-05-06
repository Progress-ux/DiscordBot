import discord
from discord.ext import commands
from discord.ui import View, Button

class HelpMenu(View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.ctx.author

    @discord.ui.button(label="🎵 Музыка", style=discord.ButtonStyle.primary, custom_id="music")
    async def music_commands(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="🎵 Музыкальные команды", color=discord.Color.blurple())
        embed.add_field(name="!play", value="Добавить трек или плейлист", inline=False)
        embed.add_field(name="!pause", value="Пауза", inline=False)
        embed.add_field(name="!resume", value="Продолжить", inline=False)
        embed.add_field(name="!stop", value="Остановить", inline=False)
        embed.add_field(name="!skip", value="Следующий трек", inline=False)
        embed.add_field(name="!back", value="Предыдущий трек", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="📜 Очередь", style=discord.ButtonStyle.secondary, custom_id="queue")
    async def queue_commands(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="📜 Управление очередью", color=discord.Color.orange())
        embed.add_field(name="!playlist", value="Текущая очередь", inline=False)
        embed.add_field(name="!history", value="История треков", inline=False)
        embed.add_field(name="!repeat", value="Повтор трека", inline=False)
        embed.add_field(name="!clear", value="Очистить очередь", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="🔊 Голос", style=discord.ButtonStyle.success, custom_id="voice")
    async def voice_commands(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(title="🔊 Голосовые команды", color=discord.Color.green())
        embed.add_field(name="!join", value="Присоединиться к каналу", inline=False)
        embed.add_field(name="!leave", value="Покинуть канал", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)


@commands.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="📚 Справка по категориям",
        description="Нажми на кнопку ниже, чтобы выбрать категорию команд:",
        color=discord.Color.green()
    )
    view = HelpMenu(ctx)
    await ctx.send(embed=embed, view=view)
