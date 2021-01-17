import discord
import json
import os
from discord.ext import commands

TOKEN = open("token.txt", "r").read()
intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
Bot = commands.Bot(command_prefix="sk!", intents=intents)


@Bot.event
async def on_ready():
    print("Bot Çalışmaya başladı")


@Bot.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open("users.json", "w") as f:
        json.dump(users, f)


async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1


async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp


async def level_up(users, user, channel):
    experience = users[user.id]['experince']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1 / 4))

    if lvl_start < lvl_end:
        await Bot.send_message(channel, '{} has leveled up to level {]'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end


@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="karşılama")
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, member)

    with open("users.json", "w") as f:
        json.dump(users, f)

    print(f"WELL CUM!!!!!!  {member} aramıza katıldı! Aileye hoş geldin {member}.")
    await channel.send(f"WELL CUM!!!!!!  {member} aramıza katıldı! Aileye hoş geldin {member}.")


@Bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="spam")
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, member)

    with open("users.json", "w") as f:
        json.dump(users, f)

    print(f"Kural bu, sen seversin o gider. {member} aramızdan ayrıldı.")
    await channel.send(f"Kural bu, sen seversin o gider. {member} aramızdan ayrıldı.")


@Bot.command()
async def kacsantim(msg):
    await msg.send("Böyle bir mezura bulunmadı efendim")


@Bot.command()
async def sumi(msg):
    await msg.send("aşığım sana..")


Bot.run(TOKEN)
