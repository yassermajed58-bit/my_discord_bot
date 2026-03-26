import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ البوت متصل الآن باسم: {bot.user.name}')

@bot.command()
async def muteall(ctx): # حذفنا سطر حماية الصلاحيات هنا للتجربة
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            if member != bot.user:
                await member.edit(mute=True)
        await ctx.send(f"🤐 تم كتم الجميع في {channel.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

@bot.command()
async def unmuteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send(f"🔊 تم فتح المايك للجميع")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

bot.run('MTQ4NjgzMjg0NjM2NTc5MDMwOQ.Gszt7k.FoLC7PqsbpdOBz8Hq-kH46ytCdyxD6u88u0W6Y')
