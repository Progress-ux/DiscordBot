from discord.ext import commands

@commands.command(name="ping", description="Send Pong!")
async def ping(ctx):
    return await ctx.respond("Pong!")