from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()

async def ping(ctx):

    """BotのPingを図るよ！"""

    ping = round(bot.latency * 1000)

    if ping > 150:

        embed = discord.Embed(title="Botのping値", description=f"**``{ping}``** ms", color=discord.Color.red())

        await ctx.reply(embed=embed)

    else:

        embed = discord.Embed(title="Botのping値", description=f"**``{ping}``** ms", color=discord.Color.green())

        await ctx.reply(embed=embed) 



       
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
