import discord
import os
from discord.ext import commands

# إعداد التصاريح (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# تعريف البوت مع البادئة (!)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ البوت متصل الآن باسم: {bot.user.name}')

# أمر كتم الجميع في الروم الصوتي
@bot.command()
async def muteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            # التأكد من عدم كتم البوت لنفسه
            if member != bot.user:
                await member.edit(mute=True)
        await ctx.send(f"🤐 تم كتم الجميع في {channel.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# أمر إلغاء كتم الجميع
@bot.command()
async def unmuteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send(f"🎙️ تم فتح المايك للجميع")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# تشغيل البوت باستخدام التوكن المخفي في Variables
token = os.environ.get('DISCORD_TOKEN')
bot.run(token)

