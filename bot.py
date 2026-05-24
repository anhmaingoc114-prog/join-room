import discord
from discord.ext import commands
import datetime
import os
import zoneinfo

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))

VN_TZ = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    server_name = guild.name if guild else "fml bụng bự"
    print(f"✅ Bot online trên server: {server_name}")


@bot.event
async def on_voice_state_update(member, before, after):
    if not GUILD_ID or member.guild.id != GUILD_ID:
        return

    now = datetime.datetime.now(VN_TZ)
    time_str = now.strftime("%H:%M")
    footer_text = f".gg/fml bụng bự • {time_str}"

    # ================== JOIN ==================
    if before.channel is None and after.channel:  
        embed = discord.Embed(
            title="🔊 Tham Gia Voice",
            description=f"{member.mention} **đã tham gia voice**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        try:
            await after.channel.send(embed=embed)
        except discord.Forbidden:
            print(f"❌ Không có quyền gửi tin nhắn trong {after.channel.name}")

    # ================== LEAVE ==================
    elif before.channel and after.channel is None:  
        embed = discord.Embed(
            title="🔇 Rời Voice",
            description=f"{member.mention} **đã rời voice**",
            color=0xff0000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        try:
            await before.channel.send(embed=embed)
        except discord.Forbidden:
            print(f"❌ Không có quyền gửi tin nhắn trong {before.channel.name}")


if not TOKEN:
    print("❌ Lỗi: Không tìm thấy TOKEN!")
else:
    bot.run(TOKEN)