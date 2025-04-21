# bot3.py
import discord
from discord import app_commands
from discord.ext import commands
from config import GUILD_ID, ALLOWED_ROLE_ID, CHANNELS, TOKENS

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

@tree.command(name="annonc", description="Отправка анонса в канал")
@app_commands.describe(
    title="Заголовок анонса",
    content="Содержание анонса",
    image_url="Ссылка на изображение (опционально)",
    mention_role="Роль для упоминания (выберите из списка, опционально)"
)
async def annonc(
    interaction: discord.Interaction,
    title: str,
    content: str,
    image_url: str = None,
    mention_role: str = None
):
    print(f"[bot3.py] Команда от {interaction.user}")

    if interaction.guild is not None:
        await interaction.response.send_message("Команда работает только в ЛС.", ephemeral=True)
        return

    guild = client.get_guild(GUILD_ID)
    if not guild:
        await interaction.response.send_message("Сервер не найден.", ephemeral=True)
        return

    member = guild.get_member(interaction.user.id)
    if not member or ALLOWED_ROLE_ID not in [r.id for r in member.roles]:
        await interaction.response.send_message("Нет доступа.", ephemeral=True)
        return

    embed = discord.Embed(title=title, description=content, color=discord.Color.green())

    if image_url:
        embed.set_image(url=image_url)
    else:
        attachments = interaction.data.get("resolved", {}).get("attachments", {})
        if attachments:
            first_attachment = list(attachments.values())[0]
            embed.set_image(url=first_attachment["url"])

    channel = client.get_channel(CHANNELS["bot3"])
    if not channel:
        await interaction.response.send_message("Канал не найден.", ephemeral=True)
        return

    mention = f"<@&{mention_role}>" if mention_role else ""
    await channel.send(
        content=mention,
        embed=embed,
        allowed_mentions=discord.AllowedMentions(roles=True)
    )

    await interaction.response.send_message("Анонс отправлен!", ephemeral=True)

@annonc.autocomplete("mention_role")
async def mention_role_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    guild = client.get_guild(GUILD_ID)
    if not guild:
        return []
    roles = [r for r in guild.roles if current.lower() in r.name.lower() and not r.is_bot_managed()]
    return [app_commands.Choice(name=r.name, value=str(r.id)) for r in roles[:25]]

@client.event
async def on_ready():
    print(f"[bot3.py] Запущен как {client.user}")
    try:
        synced = await tree.sync()
        print(f"[bot3.py] Синхронизированы команды: {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"[bot3.py] ❌ Ошибка при sync: {e}")

def run():
    client.run(TOKENS["bot3"])
