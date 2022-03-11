import os
from typing import Any
from discord.ext import commands
import json
import logging
from inputimeout import inputimeout, TimeoutOccurred

# set up logging
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# get config values from config file
try:
    with open("config.json") as f:
        config: dict = json.load(f)
    logging.info("Config file found.")
    token: str = str(config.get("token"))
    if token is None:
        logger.error("token not found in config file.")
        print("token not found in config file.")
        token = input("Please enter your token: ")
        with open("config.json", "a") as f:
            json.dump({"token": token}, f)
    user_token: str = str(config.get("user_token"))
except FileNotFoundError:
    logger.warning(
        "Config file not found. Attempting to get token from environment variables."
    )
    token = os.environ["token"]


bot = commands.Bot(command_prefix="s!")


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


@bot.command()
async def foo(ctx, arg):
    await ctx.reply(arg)


@bot.command()
async def length(ctx):
    await ctx.reply(
        "Your message is {} characters long.".format(len(ctx.message.content))
    )


@bot.command()
async def ping(ctx):
    await ctx.reply("Pong! Command took {} seconds.".format(round(bot.latency, 3)))


@bot.command()
async def test(ctx):
    await ctx.reply("Testing 1 2 3")


def run_bot(token: str, user_token: str = None):
    """
    run_bot Run the program.

    Args:
        token (str): The token to be used for the bot.
        user_token (str, optional): Token to be used for the user. Defaults to None.
    """
    try:
        mode: str = (
            inputimeout(
                prompt="Run as bot (b) or user (u)? (You have 1 second to answer)",
                timeout=1,
            )
        ).lower()
    except TimeoutOccurred:
        mode = "b"
        print("Proceeding as bot")
        logging.info("Proceeding as bot as no input was given.")
    if mode == "b":
        bot.run(token)
    elif mode == "u":
        bot.run(user_token, bot=False)
    else:
        print("Invalid mode")


run_bot(token, user_token)
