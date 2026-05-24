import discord
from discord.ext import commands
import datetime
import os
import zoneinfo

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))

VN_TZ = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")

@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD_ID)
    print(f"✅ Bot online: {bot.user}")
    print(f"📍 Server ID đã set: {GUILD_ID}")
    
    if guild:
        print(f"✅ Đã kết nối server: {guild.name} ({guild.id})")
    else:
        print("❌ Sai GUILD_ID hoặc bot chưa vào server!")

@bot.event
async def on_voice_state_update(member, before, after):
    if not GUILD_ID or member.guild.id != GUILD_ID:
        return

    now = datetime.datetime.now(VN_TZ)
    time_str = now.strftime("%H:%M")
    footer_text = f".gg/fml bụng bự • {time_str}"

    # JOIN
    if before.channel is None and after.channel:
        embed = discord.Embed(
            title="🔊 Tham Gia Voice",
            description=f"{member.mention} **đã tham gia** {after.channel.mention}",
            color=0x00ff00
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        await after.channel.send(embed=embed)

    # LEAVE
    elif before.channel and after.channel is None:
        embed = discord.Embed(
            title="🔇 Rời Voice",
            description=f"{member.mention} **đã rời** {before.channel.mention}",
            color=0xff0000
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=footer_text)

        await before.channel.send(embed=embed)


if not TOKEN:
    print("❌ Không tìm thấy TOKEN!")
else:
    bot.run(TOKEN)