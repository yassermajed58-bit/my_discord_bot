import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# تعريف البوت
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="حارس السيرفر 🤐"))
    print(f'✅ {bot.user.name} جاهز بالأوامر السريعة!')

# --- أمر الكتم (حرفين فقط: mt) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def mt(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        msg = await ctx.send("⏳ **جاري كتم الجميع...**")
        
        for i in range(3, 0, -1):
            await msg.edit(content=f"⏳ **جاري كتم الجميع خلال: {i}**")
            await asyncio.sleep(1)
        
        for member in channel.members:
            if member != ctx.author and member != bot.user:
                await member.edit(mute=True)
        
        await msg.edit(content=f"🤐 **تم الصمت! المايك لك وحده يا {ctx.author.name} 👑**")
    else:
        await ctx.send("❌ ادخل روم صوتي أولاً!")

# --- أمر الفتح (حرفين فقط: un) ---
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

# خطأ التصاريح
@mt.error
@un.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"🚫 يا {ctx.author.name}، هاي اللعبة للكبار (Admins) بس! 😂")

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
