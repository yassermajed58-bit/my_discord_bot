import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# التعديل هنا: جعلنا البريفكس فارغاً '' ليعمل الأمر بكتابة الحرفين مباشرة
bot = commands.Bot(command_prefix='', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="حارس السيرفر 🤐"))
    print(f'✅ {bot.user.name} جاهز للأوامر المباشرة!')

# --- أمر الكتم المباشر: mt ---
@bot.command()
@commands.has_permissions(administrator=True)
async def mt(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        msg = await ctx.send("⏳ **تحذير.. سيتم فرض الصمت**")
        
        for i in range(3, 0, -1):
            await msg.edit(content=f"⏳ **تحذير.. سيتم فرض الصمت خلال: {i}**")
            await asyncio.sleep(1)
        
        for member in channel.members:
            if member != ctx.author and member != bot.user:
                await member.edit(mute=True)
        
        await msg.edit(content=f"🤐 **تم الصمت! المايك لك وحدك يا {ctx.author.name} 👑**")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# --- أمر الفتح المباشر: un ---
@bot.command()
@commands.has_permissions(administrator=True)
async def un(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send("🎙️ **فتحت المايك للكل، تفضلوا احجوا!**")
    else:
        await ctx.send("❌ ادخل روم صوتي!")

# رسالة الخطأ
@mt.error
@un.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"🚫 عذراً يا {ctx.author.name}، هذا الأمر للمسؤولين فقط! 😂")

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
