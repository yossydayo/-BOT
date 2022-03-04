from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
    
class UserCog(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.group()
    async def user(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('メインコマンドの後にサブコマンドが必要です。')

    @user.command()
    async def info(self, ctx, member : discord.Member):
        users = discord.Embed(title=f'{member}の詳細', description='詳細', color=discord.Color.orange())
        users.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        users.set_thumbnail(url=member.avatar_url)
        users.add_field(name='名前', value=f'**{member.display_name}#{member.discriminator}**')
        users.add_field(name='あなたはBot?', value=member.bot)
        users.add_field(name='作成時間', value=member.created_at, inline=False)
        users.add_field(name='サーバーに参加した時間', value=member.joined_at)
        await ctx.send(embed=users)

    @user.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, reason=None):
        kick = discord.Embed(title='メンバーをキックしました', description='Kickしたメンバーにまた来てもらうには再招待してください', color=discord.Color.red())
        kick.add_field(name='執行人', value=f'{ctx.author.mention}')
        kick.add_field(name='Kickされた人', value=f'{member.mention}')
        kick.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=kick)
        await member.kick(reason=reason)

    @user.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member : discord.Member, reason=None):
        ban = discord.Embed(title='メンバーをBANしました', description='BANしたメンバーにまた来てもらうにはUNBANをし再招待してください', color=discord.Color.red())
        ban.add_field(name='執行人', value=f'{ctx.author.mention}')
        ban.add_field(name='Kickされた人', value=f'{member.mention}')
        ban.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=ban)
        await member.ban(reason=reason)

    @user.command()
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, member : discord.Member, reason=None):
        unban=discord.Embed(title="BANを解除しました", color=0xff0000)
        unban.set_thumbnail(url=user.avatar_url)
        unban.add_field(name="対象", value=user, inline=False)
        unban.add_field(name="実行", value=ctx.author, inline=False)
        await user.unban()
        await ctx.channel.send(embed=unban)

def setup(bot):
    bot.add_cog(UserCog(bot))
    
@bot.command()
async def ping(ctx):
    await ctx.send('🏓pong!')
    
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
