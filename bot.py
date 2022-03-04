import json
import logging

import discord

# get config values from config file
with open("config.json") as f:
    config = json.load(f)

token = config.get("token")

# set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

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
