import discord
import os
import asyncio
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
                
                # إرسال رسالة عادية (ليست مخفية) حتى نتمكن من حذفها
                await interaction.response.send_message("🤐 تم كتم الجميع.. بالتوفيق!")
                msg = await interaction.original_response()
                await asyncio.sleep(3)
                await msg.delete()
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
                
                # إرسال رسالة عادية وحذفها بعد 3 ثواني
                await interaction.response.send_message("🎙️ المايك مفتوح.. منو القاتل؟")
                msg = await interaction.original_response()
                await asyncio.sleep(3)
                await msg.delete()
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 للأدمن فقط!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="تحريات Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز للحذف التلقائي!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="استخدم الأزرار للتحكم السريع. (الرسائل ستحذف تلقائياً)",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
