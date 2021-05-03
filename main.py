#!/usr/bin/python3
"""
Title:			Main
Type:			Main Program
Purpose:		Start the whole thing!
Author: 		AG | MuirlandOracle
Last Updated:	03/05/2021 (AG | MuirlandOracle)
"""
import discord, asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument
from libs.loadconf import config, secrets
from libs.colours import Colours


bot = commands.Bot(command_prefix=config["prefix"])
bot.remove_command("help")


#Load the cogs
for cog in config["cogs"]:
	if cog not in config["disabledCogs"]:
		try:
			bot.load_extension(f"cogs.{cog}")
			Colours.success(f"{cog} loaded successfully")
		except Exception as e:
			Colours.warn(f"{cog} failed to load: {e}")
	else:
		Colours.info(f"Skipping {cog}")


#On Ready confirmation
@bot.event
async def on_ready():
	if config["status"] != "":
		await bot.change_presence(activity=discord.Game(config["status"]))
	Colours.success("Bot Started!")

#Ignore the annoying errors
@bot.event
async def on_command_error(ctx, error):
	error_to_skip = [CommandNotFound, MissingRequiredArgument]
	for error_type in error_to_skip:
		if isinstance(error, error_type):
			return
	raise error



try:
	bot.run(secrets["token"])
except RuntimeError:
	exit()