import discord
import os
from discord.ext import commands

# 1. إعداد التصاريح
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ البوت متصل الآن باسم: {bot.user.name}')

# --- أمر كتم الجميع ما عدا "أنت" (للمسؤولين فقط) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def muteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            # هنا التعديل: إذا كان العضو هو "أنت" أو "البوت نفسه" لا يكتمه
            if member != ctx.author and member != bot.user:
                await member.edit(mute=True)
        
        await ctx.send(f"🤐 تم كتم الجميع في {channel.name}.. المايك الآن لك وحده يا {ctx.author.name}! 👑")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً لتنفيذ الأمر!")

# --- أمر إلغاء كتم الجميع ---
@bot.command()
@commands.has_permissions(administrator=True)
async def unmuteall(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send(f"🎙️ تم فتح المايك للجميع بطلب من {ctx.author.name}")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# رسالة الخطأ للمتطفلين
@muteall.error
@unmuteall.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"🚫 عذراً يا {ctx.author.name}، هذا الأمر للقادة (Administrator) فقط! ✋")

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
