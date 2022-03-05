import asyncio
import json
import logging

import discord

with open("config.json") as f:
    config = json.load(f)
token = config.get("token")


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class MyClient(discord.Client):
    async def on_ready(self):
        print("Connected!")
        print("Username: {0.name}\nID: {0.id}".format(self.user))

    async def on_message(self, message):
        if message.content.startswith("!editme"):
            msg = await message.channel.send("10")
            await asyncio.sleep(3.0)
            await msg.edit(content="40")

    async def on_message_edit(self, before, after):
        fmt = "**{0.author}** edited their message:\n{0.content} -> {1.content}"
        await before.channel.send(fmt.format(before, after))


client = MyClient()
client.run(token, bot=False)
