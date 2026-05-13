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
    server_name = guild.name if guild else "Thế Giới Ảo"
    print(f"✅ Bot online trên server: {server_name}")


@bot.event
async def on_voice_state_update(member, before, after):
    guild = bot.get_guild(GUILD_ID)
    
    now = datetime.datetime.now(VN_TZ)
    time_str = now.strftime("%H:%M")

    # Tự động lấy tên server thật + giữ .gg/
    server_name = guild.name if guild else "Server"
    clean_name = server_name.replace(" ", "").lower()   # bỏ dấu cách, viết thường
    footer_text = f".gg/{clean_name} • Hôm nay lúc {time_str}"

    if before.channel is None and after.channel:   # JOIN
        embed = discord.Embed(
            title="Tham Gia Voice Chat",
            description=f"{member.mention} **đã tham gia voice chat**",
            color=0x00ff00
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        await after.channel.send(embed=embed)

    elif before.channel and after.channel is None:   # LEAVE
        embed = discord.Embed(
            title="Rời Voice Chat",
            description=f"{member.mention} **đã rời voice chat**",
            color=0xff0000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        await before.channel.send(embed=embed)


if not TOKEN:
    print("❌ Lỗi: Không tìm thấy TOKEN! Hãy set biến môi trường TOKEN trên Railway.")
else:
    bot.run(TOKEN)