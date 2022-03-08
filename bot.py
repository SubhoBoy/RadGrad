from typing import Any
from discord.ext import commands
import json
import logging

# get config values from config file
with open("config.json") as f:
    config: dict = json.load(f)

token: Any = config.get("token")
user_token: Any = config.get("user_token")

# set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="logs/new.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


bot = commands.Bot(command_prefix="!")


async def get_wanted_channel(server: str, channel: str) -> Any:
    """Get a specific channel from a specific server.

    Args:
        server (string): Part of the server name.
        channel (string): Part of the channel name.
    """
    guilds = bot.guilds
    for current_guild in guilds:
        if server in current_guild.name.lower():
            channels = current_guild.channels
            for current_channel in channels:
                if channel in current_channel.name.lower():
                    return current_channel


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    print("Press Ctrl+C to stop")


# @bot.event
# async def on_message(message):
#     if message.channel == wanted_channel:
#         if message.content == "!test":
#             await message.channel.send("Testing 1 2 3")
#         await bot.process_commands(message)


@bot.command()
async def foo(ctx, arg):
    await ctx.send(arg)


@bot.command()
async def length(ctx):
    await ctx.send(
        "Your message is {} characters long.".format(len(ctx.message.content))
    )


mode = (input("Run as bot (b) or run as user (u)? ")).lower()
if mode == "b":
    bot.run(token)
elif mode == "u":
    bot.run(user_token, bot=False)
else:
    print("Invalid mode")
