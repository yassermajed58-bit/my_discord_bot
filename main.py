import discord
import os
from discord.ext import commands

# 1. إعداد التصاريح (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# 2. تعريف البوت مع البريفكس '!'
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ البوت متصل الآن باسم: {bot.user.name}')

# --- أمر كتم الجميع (للمسؤولين فقط) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def muteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            if member != bot.user: # التأكد من عدم كتم البوت لنفسه
                await member.edit(mute=True)
        await ctx.send(f"🤐 تم كتم الجميع في 🔊 {channel.name} بواسطة المسؤول {ctx.author.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# --- أمر إلغاء كتم الجميع (للمسؤولين فقط) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def unmuteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send(f"🎙️ تم فتح المايك للجميع بواسطة المسؤول {ctx.author.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# --- التعامل مع الأخطاء (إذا حاول شخص غير مسؤول استخدام الأمر) ---
@muteall.error
@unmuteall.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"🚫 عذراً يا {ctx.author.name}، هذا الأمر للمسؤولين (Administrator) فقط! ✋")

# 3. تشغيل البوت باستخدام التوكن المخفي في Railway
token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
