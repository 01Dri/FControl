import discord
import asyncio
import os

from discord.ext import commands
from dotenv import load_dotenv
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
message_user = {}

def get_embed_flood(content):
    return discord.Embed(
                title="Aviso de Flood",
                description=content,
                color=discord.Color.red())

@bot.event
async def on_ready():
    print('Bot está pronto!')



@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if not message.author.guild_permissions.administrator:
        
        if message.author.name not in message_user:
            message_user[message.author.name] = {}

        message_content = message.content

        if list(message_user[message.author.name].values()).count(message_content) == 3:

            await message.channel.send(embed=get_embed_flood(f"O usuário {message.author.mention} foi banido! MOTIVO: Flood"))
            await message.author.ban(reason="SPAM")
            message_user[message.author.name].clear()
            return

        if list(message_user[message.author.name].values()).count(message_content) == 2:
            await message.channel.send(embed=get_embed_flood(f"{message.author.mention} Você está enviando mensagens repetidas, se continuar será banido!"))

        if message.channel.name in message_user[message.author.name]:
            if message.content == message_user[message.author.name][message.channel.name]:
                await message.delete()
                await message.channel.send(embed=get_embed_flood(f"{message.author.mention} Você está temporiariamente impedido de mandar mensagens!!"))
                await message.channel.set_permissions(message.author, send_messages=False)
                await asyncio.sleep(60)
                await message.channel.set_permissions(message.author, send_messages=True)

        else:
            message_user[message.author.name][message.channel.name] = message.content

        print(message_user)

        await asyncio.sleep(60)
        if message.author.name in message_user:
            del message_user[message.author.name]

load_dotenv()
bot.run(os.getenv("TOKEN_DISCORD"))
