import discord
from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix=',')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="現在コマンド反応しません。"), status=discord.Status.dnd) 


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send(':ping_pong:pong!')
    
@bot.event
async def on_message(message):
  if '@everyone' in message.content:
    await message.channel.send('えぶりわんするなよ！しね！') 

token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)