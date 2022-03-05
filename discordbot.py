from http import client
from pydoc import cli
import discord
from discord.ext import commands
import random
from discord import Permissions
from colorama import Fore, Style
import asyncio
from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix=',')

@client.event
async def on_ready():
  print('Logged in as')
  await client.change_presence(activity=discord.Game(name="online now"))

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    
@bot.command()
async def ping(ctx):
    await ctx.send('🏓pong!')
    
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token) 
