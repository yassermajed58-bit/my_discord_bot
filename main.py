import discord
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="حارس السيرفر 🤐"))
    print(f'✅ {client.user.name} جاهز للأوامر المباشرة (mt/un)!')

@client.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author == client.user:
        return

    # تحويل الرسالة لنص صغير للتأكد
    content = message.content.lower().strip()

    # --- أمر الكتم المباشر: mt ---
    if content == 'mt':
        if message.author.guild_permissions.administrator:
            if message.author.voice:
                channel = message.author.voice.channel
                msg = await message.channel.send("⏳ **تنبيه.. الصمت يقترب**")
                
                for i in range(3, 0, -1):
                    await msg.edit(content=f"⏳ **تنبيه.. الصمت يقترب خلال: {i}**")
                    await asyncio.sleep(1)
                
                for member in channel.members:
                    if member != message.author and member != client.user:
                        await member.edit(mute=True)
                
                await msg.edit(content=f"🤐 **تم الصمت! المايك لك وحده يا {message.author.name} 👑**")
            else:
                await message.channel.send("❌ ادخل روم صوتي أولاً!")
        else:
            await message.channel.send(f"🚫 يا {message.author.name}، هاي اللعبة للأدمن بس! 😂")

    # --- أمر الفتح المباشر: un ---
    elif content == 'un':
        if message.author.guild_permissions.administrator:
            if message.author.voice:
                channel = message.author.voice.channel
                for member in channel.members:
                    await member.edit(mute=False)
                await message.channel.send("🎙️ **فتحت المايك للكل، تفضلوا احجوا!**")
            else:
                await message.channel.send("❌ ادخل روم صوتي!")

# تشغيل البوت
token = os.environ.get('DISCORD_TOKEN')
client.run(token)
