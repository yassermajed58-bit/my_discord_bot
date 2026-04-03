import discord
import os
import asyncio
from discord.ext import commands
from discord.ui import View, button

# الـ ID مالت روم اللوق
LOG_CHANNEL_ID = 1489596321580060732

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# غيرنا البريفكس هنا إلى نقطة .
bot = commands.Bot(command_prefix='.', intents=intents)

class AmongUsControl(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="كتم الكل 🔴", style=discord.ButtonStyle.danger, custom_id="mute_all_btn")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        if interaction.user.voice and interaction.user.voice.channel:
            channel = interaction.user.voice.channel
            count = 0
            for member in channel.members:
                if member != interaction.user and not member.bot:
                    try:
                        await member.edit(mute=True)
                        count += 1
                    except: continue
            
            log_chan = bot.get_channel(LOG_CHANNEL_ID)
            if log_chan:
                await log_chan.send(f"🤐 **لوق:** تم كتم `{channel.name}` بواسطة {interaction.user.name}")
            
            await interaction.followup.send(f"✅ تم كتم {count} أعضاء.", ephemeral=True)
        else:
            await interaction.followup.send("❌ ادخل روم صوتي أولاً!", ephemeral=True)

    @discord.ui.button(label="فتح الكل 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all_btn")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        if interaction.user.voice and interaction.user.voice.channel:
            channel = interaction.user.voice.channel
            count = 0
            for member in channel.members:
                try:
                    await member.edit(mute=False)
                    count += 1
                except: continue
            
            log_chan = bot.get_channel(LOG_CHANNEL_ID)
            if log_chan:
                await log_chan.send(f"🎙️ **لوق:** تم فتح `{channel.name}` بواسطة {interaction.user.name}")
            
            await interaction.followup.send(f"✅ تم فتح المايكات لـ {count} أعضاء.", ephemeral=True)

@bot.event
async def on_ready():
    print(f'✅ {bot.user.name} جاهز! استخدم .setup')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="اضغط الأزرار للتحكم.\nالتقارير تروح لروم اللوق الخاص.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
