import json

import discord

with open("config.json") as f:
    config = json.load(f)

token = config.get("token")


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        print(message.author)

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


client.run(
    token,
    bot=False,
)
