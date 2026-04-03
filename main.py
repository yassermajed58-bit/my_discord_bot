import discord
import os
import asyncio
from discord.ext import commands
from discord.ui import View

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

class AmongUsControl(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="كتم الكل (بدأ اللعب) 🔴", style=discord.ButtonStyle.danger, custom_id="mute_all")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # استجابة فورية لمنع الـ Failed
        await interaction.response.send_message("⏳ جاري الكتم...", ephemeral=True, delete_after=1)
        
        if interaction.user.guild_permissions.administrator and interaction.user.voice:
            channel = interaction.user.voice.channel
            for member in channel.members:
                if member != interaction.user and not member.bot:
                    try: await member.edit(mute=True)
                    except: continue
            
            # إرسال رسالة التأكيد وحذفها بعد 10 ثوانٍ
            msg = await interaction.channel.send(f"🤐 **تم كتم الجميع بأمر {interaction.user.name}**")
            await asyncio.sleep(10)
            try: await msg.delete()
            except: pass

    @discord.ui.button(label="فتح الكل (إجتماع) 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # استجابة فورية لمنع الـ Failed
        await interaction.response.send_message("⏳ جاري فتح المايكات...", ephemeral=True, delete_after=1)
        
        if interaction.user.guild_permissions.administrator and interaction.user.voice:
            channel = interaction.user.voice.channel
            for member in channel.members:
                if not member.bot:
                    try: await member.edit(mute=False)
                    except: continue
            
            # إرسال رسالة التأكيد وحذفها بعد 10 ثوانٍ
            msg = await interaction.channel.send(f"🎙️ **فتحت المايكات.. منو الـ Impostor؟**")
            await asyncio.sleep(10)
            try: await msg.delete()
            except: pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="تحريات Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز ومؤقت الحذف: 10 ثوانٍ!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="استخدم الأزرار للتحكم السريع.\n(الرسائل ستحذف تلقائياً بعد 10 ثوانٍ)",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
