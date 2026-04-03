import discord
import os
import asyncio # ضروري للمؤقت
from discord.ext import commands
from discord.ui import Button, View

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
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                for member in channel.members:
                    if member != interaction.user and member != bot.user:
                        await member.edit(mute=True)
                
                # إرسال رسالة وحذفها بعد 3 ثواني
                msg = await interaction.response.send_message(f"🤐 تم الكتم بأمر {interaction.user.name}")
                await asyncio.sleep(3)
                await interaction.delete_original_response()
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 للأدمن فقط!", ephemeral=True)

    @discord.ui.button(label="فتح الكل (إجتماع) 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                for member in channel.members:
                    await member.edit(mute=False)
                
                # إرسال رسالة وحذفها بعد 3 ثواني
                msg = await interaction.response.send_message(f"🎙️ المايك مفتوح للكل!")
                await asyncio.sleep(3)
                await interaction.delete_original_response()
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 للأدمن فقط!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="تحريات Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="استخدم الأزرار للتحكم السريع بالصوت.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
