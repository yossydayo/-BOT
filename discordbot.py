import discord
from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix=',')

@bot.event
async def on_ready():
  print('ろぐいんなう')
  await bot.change_presence(activity=discord.Game(name="現在コマンド反応しません。"))

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send(':ping_pong:pong!')

@bot.command()
async def @everyone(ctx):
  await ctx.send('えぶりわんするなやしね！')

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)