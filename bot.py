import os
from random import random
from typing import Any
from discord.ext import commands
import json
import logging
from inputimeout import inputimeout, TimeoutOccurred
import sys
import keep_alive

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
    logger.info("Config file found.")
    token: str = str(config.get("token"))
    if token is None:
        logger.error("token not found in config file.")
        print("token not found in config file.")
        token = input("Please enter your token: ")
        with open("config.json", "a") as f:
            json.dump({"token": token}, f)
    user_token: Any = str(config.get("user_token"))
except FileNotFoundError:
    logger.warning(
        "Config file not found. Attempting to get token from environment variables."
    )
    try:
        token = os.environ["token"]
    except KeyError:
        logger.critical("token not found in environment variables. Exiting.")
        sys.exit(
            """no token found.
            Please enter a token in config file or environment variable."""
        )
    try:
        user_token = os.environ["user_token"]
    except KeyError:
        logger.info("user_token not found in environment variables.")
        user_token = None


bot = commands.Bot(command_prefix="s!")


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
        "Your message is {} characters long.".format(len(ctx.message.content) - 9)
    )


@bot.command()
async def ping(ctx):
    await ctx.reply("Pong! Command took {} seconds.".format(round(bot.latency, 3)))


@bot.command()
async def test(ctx):
    await ctx.reply("Testing 1 2 3")


@bot.command(name="8ball")
async def eight_ball(ctx):
    choices = [
        "Yes, definetely.",
        "No, certainly not.",
        "This question peers too deep into the mystical depths of the universe.",
        "Why would you even ask that?",
        "You are not yet qualified to ask that question. Try skiing or something.",
    ]
    if ctx.message.content.lower() is ("s!8ball" or "s!8ball "):
        await ctx.reply("Please ask a question.")
    else:
        await ctx.reply(random.choice(choices))


@commands.command(name="help", aliases=["man"])
async def help(self, ctx: commands.Context):
    await ctx.send("template command")


def run_bot(token: str, user_token: str = None):
    """
    Run the program.

    Args:
        token (str): The token to be used for the bot.
        user_token (str, optional): Token to be used for the user. Defaults to None.
    """
    try:
        mode: str = (
            inputimeout(
                prompt="Run as bot (b) or user (u)? (You have 3 seconds to answer)",
                timeout=3,
            )
        ).lower()
    except TimeoutOccurred:
        mode = "b"
        print("Proceeding as bot")
        logger.info("Proceeding as bot as no input was given.")
    if mode == "b":
        bot.run(token)
    elif mode == "u":
        bot.run(user_token, bot=False)
    else:
        print("Invalid mode")


keep_alive.keep_alive()
run_bot(token, user_token)
