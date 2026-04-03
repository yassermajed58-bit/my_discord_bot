import discord
import os
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

    # زر الكتم
    @discord.ui.button(label="كتم الكل (بدأ اللعب) 🔴", style=discord.ButtonStyle.danger, custom_id="mute_all")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                await interaction.response.defer() # تأكيد الاستلام فوراً
                channel = interaction.user.voice.channel
                for member in channel.members:
                    if member != interaction.user and not member.bot:
                        try:
                            await member.edit(mute=True)
                        except: continue
                await interaction.followup.send(f"🤐 **تم كتم الجميع بأمر {interaction.user.name}**")
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي أولاً!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 للأدمن فقط!", ephemeral=True)

    # زر الفتح
    @discord.ui.button(label="فتح الكل (إجتماع) 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.administrator:
            if interaction.user.voice:
                await interaction.response.defer() # تأكيد الاستلام فوراً
                channel = interaction.user.voice.channel
                for member in channel.members:
                    if not member.bot:
                        try:
                            await member.edit(mute=False)
                        except: continue
                await interaction.followup.send(f"🎙️ **فتحت المايكات.. منو الـ Impostor؟**")
            else:
                await interaction.response.send_message("❌ ادخل روم صوتي أولاً!", ephemeral=True)
        else:
            await interaction.response.send_message("🚫 للأدمن فقط!", ephemeral=True)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="تحريات Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز وشغال تمام!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="استخدم الأزرار بالأسفل للتحكم بالصوت أثناء اللعب.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
