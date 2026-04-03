import discord
import os
import asyncio
from discord.ext import commands

# ID روم اللوك مالتك
LOG_CHANNEL_ID = 1489596321580060732

# تفعيل كل الحساسات برمجياً
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='', intents=intents) # بدون بريفكس حتى تكتب mt مباشرة

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} دخل الخدمة يا شنشول!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower().strip()

    # --- أمر الكتم السريع mt ---
    if content == 'mt':
        if message.author.voice:
            # مسح كلمة mt فوراً حتى ما تخرب الشات
            try: await message.delete()
            except: pass
            
            channel = message.author.voice.channel
            count = 0
            # نجلب الأعضاء بطريقة "الفريش"
            members = channel.members
            for member in members:
                if member != message.author and not member.bot:
                    try:
                        await member.edit(mute=True)
                        count += 1
                    except: continue
            
            # إرسال التقرير لروم اللوك
            log_chan = bot.get_channel(LOG_CHANNEL_ID)
            if log_chan:
                await log_chan.send(f"🤐 **كتم جماعي:** تم كتم `{count}` لاعبين في `{channel.name}` بواسطة {message.author.name}")
        
    # --- أمر الفتح السريع un ---
    elif content == 'un':
        if message.author.voice:
            try: await message.delete()
            except: pass
            
            channel = message.author.voice.channel
            count = 0
            for member in channel.members:
                if not member.bot:
                    try:
                        await member.edit(mute=False)
                        count += 1
                    except: continue
            
            log_chan = bot.get_channel(LOG_CHANNEL_ID)
            if log_chan:
                await log_chan.send(f"🎙️ **فتح جماعي:** المايكات انفتحت لـ `{count}` لاعبين بواسطة {message.author.name}")

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
