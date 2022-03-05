from discord import Embed
from discord.ext.commands import Bot, Cog, command, Context
from datetime import timedelta, datetime as d
from random import randint, choice
from googletrans import Translator
from lib import checker, data as s
from json import loads
from threading import Thread
from asyncio import sleep

class Game(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot

	def translate(self, num, arg, args):
		for n in range(1, 4):
			try:
				translator = Translator()
				translator.translate('hello', dest='ja')
				break
			except Exception as e:
				self.bot.log(4, e)
				self.bot.log(4, f'Retrying... ({n})')
			if n == 3:
				raise Exception
		try:
			result = []
			self.bot.data['rev'][num]['start'] = d.utcnow().timestamp()
			lang = choice(s.language)
			temp1 = translator.translate(args, dest=lang)
			temp2 = translator.translate(temp1.text, dest='ja')
			result.append(temp2.text)
			self.bot.data['rev'][num]['progress'] = 1
			self.bot.data['rev'][num]['duration'] = d.utcnow().timestamp()
			for n in range(1, arg):
				if not num in self.bot.data['rev']:
					return
				lang = choice(s.language)
				temp1 = translator.translate(temp1.text, dest=lang)
				temp2 = translator.translate(temp1.text, dest='ja')
				result.append(temp2.text)
				if checker.debug == True:
					self.bot.log(3, f'{temp1.text} > {temp2.text} (lang : {lang} > ja))')
				self.bot.data['rev'][num]['progress'] = n+1
				self.bot.data['rev'][num]['duration'] = d.utcnow().timestamp()
			self.bot.data['rev'][num]['result'] = result
		except Exception as e:
			self.bot.log(4, e)
			self.bot.data['rev'][num]['error'] = True

	@command(aliases=['rev', 're', 'reversetranslate'])
	async def reversetranslation(self, ctx: Context, arg: int, *, args: str):
		if len(self.bot.data['rev']) >= 20:
			await ctx.reply('Thread Count Reached Limit. Try again later.')
			self.bot.data['smessages'] += 1
			return
		embed = Embed(title='逆翻訳しています...', colour=s.color1, timestamp=d.utcnow())
		embed.add_field(name='進行状況', value='0/{} (0.0%)'.format(arg), inline=False)
		embed.add_field(name='予想残り時間', value='計算中', inline=False)
		message = await ctx.reply(embed=embed, mention_author=False)
		self.bot.data['smessages'] += 1
		num = len(self.bot.data['rev'])+1
		self.bot.data['rev'][num] = {'duration': None, 'progress': 0, 'result': None, 'error': False}
		self.bot.log(1, self.bot.data['rev'])
		try:
			thread = Thread(target=self.translate, args=([num, arg, args]), name=f'thread-{num}')
			thread.start()
			count = 0
			while not self.bot.data['rev'][num]['result']:
				await sleep(3)
				try:
					embed = Embed(title='逆翻訳しています...', colour=s.color1, timestamp=d.utcnow())
					temp = self.bot.data['rev'][num]['progress']
					progress = float(temp / arg) * 100
					duration = int(float(float(self.bot.data['rev'][num]['duration'] - self.bot.data['rev'][num]['start']) / temp) * int(arg - temp))
					embed.add_field(name='進行状況', value=f'{temp}/{arg} ({progress:.1f}%)', inline=False)
					if not duration:
						embed.add_field(name='予想残り時間', value='計算中', inline=False)
					else:
						embed.add_field(name='予想残り時間', value=timedelta(seconds=duration), inline=False)
					await message.edit(content=None, embed=embed, allowed_mentions=self.bot.mention)
				except:
					pass
				if self.bot.data['rev'][num]['error']:
					raise Exception
		except Exception as e:
			self.bot.log(4, e)
			del self.bot.data['rev'][num]
			await ctx.reply(content='Failed in Finalizing.')
			return
		embed = Embed(title='逆翻訳しています...', colour=s.color1, timestamp=d.utcnow())
		embed.add_field(name='進行状況', value='{0}/{0} (100%)'.format(arg), inline=False)
		embed.add_field(name='予想残り時間', value='完了', inline=False)
		await message.edit(content=None, embed=embed, allowed_mentions=self.bot.mention)
		finalize = []
		finalize2 = []
		finalize.append('{}\n'.format(args))
		for n in range(len(self.bot.data['rev'][num]['result'])):
			if 4000 - len(''.join(finalize)) - len(self.bot.data['rev'][num]['result'][n]) >= 100:
				finalize.append('\n{}. {}'.format(n+1, self.bot.data['rev'][num]['result'][n]))
			elif 4000 - len(''.join(finalize2)) - len(self.bot.data['rev'][num]['result'][n]) >= 100:
				finalize2.append('{}. {}\n'.format(n+1, self.bot.data['rev'][num]['result'][n]))
			else:
				del self.bot.data['rev'][num]
				await ctx.reply(content='Error : The result is over 8000 characters.')
				self.bot.data['smessages'] += 1
				return
		del self.bot.data['rev'][num]
		await ctx.reply(embed=Embed(title='Result', description=''.join(finalize), colour=0x7ED6DE, timestamp=d.utcnow()), mention_author=False)
		self.bot.data['smessages'] += 1
		if len(finalize2) != 0:
			await ctx.send(embed=Embed(title='Result', description=''.join(finalize2)[:-1], colour=0x7ED6DE, timestamp=d.utcnow()))
			self.bot.data['smessages'] += 1

	@command(aliases=[])
	async def omikuji(self, ctx: Context):
		now = d.now()
		match = loads(open('data/match.json', 'r').read())
		author = str(ctx.author.id)[-3:]
		value = int(str(int(author) ** now.day)[-1:])
		omikuji = ['大吉', '中吉', '小吉', '吉', '末吉', '凶']#大吉・中吉・小吉・吉・末吉・凶
		if value == 0:
			result = omikuji[0]
		if value == 1:
			result = omikuji[2]
		if value == 2:
			result = omikuji[4]
		if value == 3:
			result = omikuji[1]
		if value == 4:
			result = omikuji[2]
		if value == 5:
			result = omikuji[0]
		if value == 6:
			result = omikuji[5]
		if value == 7:
			result = omikuji[1]
		if value == 8:
			result = omikuji[3]
		if value == 9:
			result = omikuji[3]
		embed = Embed(title='おみくじ', description='{}の結果\n\n`{}`'.format(now.strftime('%Y/%m/%d'), result), colour=s.color1, timestamp=d.utcnow())
		await ctx.send(embed=embed)
		self.bot.data['smessages'] += 1

	@command(aliases=[])
	async def say(self, ctx: Context, arg):
		await ctx.send(arg)
		self.bot.data['smessages'] += 1

	@command(aliases=['randint'])
	async def random(self, ctx: Context, start:int, end:int):
		await ctx.send(str(randint(start,end)))
		self.bot.data['smessages'] += 1

	@command(aliases=['pick'])
	async def choice(self, ctx: Context, *, arg:str):
		await ctx.send(str(choice(arg.split(' '))))
		self.bot.data['smessages'] += 1

def setup(bot: Bot):
    bot.add_cog(Game(bot))
