import discord
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="حارس Among Us 🕵️"))
    print(f'✅ {client.user.name} جاهز للأوامر (mt/un) بدون حذف!')

@client.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author == client.user:
        return

    content = message.content.lower().strip()

    # --- أمر الكتم المباشر: mt ---
    if content == 'mt':
        if message.author.guild_permissions.administrator:
            if message.author.voice:
                channel = message.author.voice.channel
                for member in channel.members:
                    if member != message.author and not member.bot:
                        try:
                            await member.edit(mute=True)
                        except: continue
                
                await message.channel.send(f"🤐 **تم كتم الجميع.. العبوا بصمت!** (بأمر {message.author.name} 👑)")
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
                    if not member.bot:
                        try:
                            await member.edit(mute=False)
                        except: continue
                
                await message.channel.send(f"🎙️ **فتحت المايك للكل، تفضلوا احجوا!** (بأمر {message.author.name} ✨)")
            else:
                await message.channel.send("❌ ادخل روم صوتي أولاً!")
        else:
            await message.channel.send(f"🚫 للأدمن فقط!")

# تشغيل البوت
token = os.environ.get('DISCORD_TOKEN')
client.run(token)
