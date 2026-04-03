import discord
import os
import asyncio
from discord.ext import commands
from discord.ui import View

# الـ ID مالت روم اللوق اللي انطيتني اياه
LOG_CHANNEL_ID = 1489596321580060732

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

class AmongUsControl(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="كتم الكل 🔴", style=discord.ButtonStyle.danger, custom_id="mute_all")
    async def mute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # رد فوري مخفي لمنع الـ Failed
        await interaction.response.send_message("⏳ جاري الكتم...", ephemeral=True, delete_after=1)
        
        if interaction.user.guild_permissions.administrator and interaction.user.voice:
            channel = interaction.user.voice.channel
            for member in channel.members:
                if member != interaction.user and not member.bot:
                    try: await member.edit(mute=True)
                    except: continue
            
            # إرسال التقرير لروم اللوك فقط
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(title="🤐 تم الكتم", color=discord.Color.red())
                embed.add_field(name="الروم الصوتي", value=channel.name, inline=True)
                embed.add_field(name="بواسطة", value=interaction.user.name, inline=True)
                await log_channel.send(embed=embed)

    @discord.ui.button(label="فتح الكل 🟢", style=discord.ButtonStyle.success, custom_id="unmute_all")
    async def unmute_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # رد فوري مخفي لمنع الـ Failed
        await interaction.response.send_message("⏳ جاري الفتح...", ephemeral=True, delete_after=1)
        
        if interaction.user.guild_permissions.administrator and interaction.user.voice:
            channel = interaction.user.voice.channel
            for member in channel.members:
                if not member.bot:
                    try: await member.edit(mute=False)
                    except: continue
            
            # إرسال التقرير لروم اللوك فقط
            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                embed = discord.Embed(title="🎙️ تم الفتح", color=discord.Color.green())
                embed.add_field(name="الروم الصوتي", value=channel.name, inline=True)
                embed.add_field(name="بواسطة", value=interaction.user.name, inline=True)
                await log_channel.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="إدارة Among Us 🔍"))
    print(f'✅ {bot.user.name} جاهز ونظام الأزرار مع اللوق شغال!')

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    embed = discord.Embed(
        title="🎮 لوحة تحكم Among Us",
        description="الأوامر تتنفذ هنا، والتقارير تروح لروم اللوك الخاص.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=AmongUsControl())

token = os.environ.get('DISCORD_TOKEN')
bot.run(token)
