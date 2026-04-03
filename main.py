import discord
import os
from discord.ext import commands
from discord.ui import Button, View # أضفنا نظام الأزرار

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- واجهة الأزرار ---
class AmongUsControl(View):
    def __init__(self):
        super().__init__(timeout=None) # الأزرار تبقى شغالة للأبد

    # زر كتم الجميع (وقت اللعب)
    @discord.ui.button(label="كتم الكل (بدأ اللعب) 🔴", style=discord.ButtonStyle.danger, custom_id="mute_all")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                for member in channel.members:
                    if member != interaction.user and member != bot.user:
                        await member.edit(mute=True)
                await interaction.response.send_message(f"🤐 تم كتم الجميع.. العبوا بصمت! (بأمر {interaction.user.name})", ephemeral=True)
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي أولاً!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 هاي للأدمن بس يا بطل! 😂", ephemeral=True)

    # زر فتح الجميع (وقت الاجتماع)
    @discord.ui.button(label="فتح الكل (إجتماع) 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                channel = interaction.user.voice.channel
                for member in channel.members:
                    await member.edit(mute=False)
                await interaction.response.send_message(f"🎙️ المايك مفتوح.. منو الـ Impostor؟ 🔥", ephemeral=True)
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي أولاً!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 هاي للأدمن بس يا بطل! 😂", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="تحريات Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز بالأزرار!')

# --- أمر إظهار لوحة التحكم ---
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="استخدم الأزرار بالأسفل للتحكم بالمايكات بسرعة أثناء اللعب.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
