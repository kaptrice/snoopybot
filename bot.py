import json
import os
import platform
import random
import sys
import asyncio
from datetime import datetime, time, timedelta
import aiohttp
import exceptions



import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

with open("config.json") as file:
    config = json.load(file)


intents = disnake.Intents.default()
intents.message_content = True
bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents, help_command=None)
bot.config = config
host = "data.usajobs.gov"
authKey  = "" #your api key goes here
userAgent  = "" #the email with which the key was registered
headers = {"Host":host, "User-Agent":userAgent, "Authorization-Key":authKey}

WHEN = time(0, 0, 0)


@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=disnake.CustomActivity("Administrating they air and space")) #status!
    print(f"Logged in as {bot.user.name}")
    print("-------------------")

def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    """
    The code in this event is executed every time a slash command has been *successfully* executed
    :param interaction: The slash command that has been executed.
    """
    print(
        f"Executed {interaction.data.name} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    """
    The code in this event is executed every time a valid slash command catches an error

    'ephemeral=True' will make so that only the user who execute the command can see the message

    :param interaction: The slash command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)

    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await interaction.send(embed=embed, ephemeral=True)

    elif isinstance(error, exceptions.ChannelNotInList):
        """
        Used when channelnotinlist exception thrown
        """
        embed = disnake.Embed(
            description="That channel already isn't used for notifications!",
            color=0xE02B2B
        )
        await interaction.send(embed=embed)
        bot.logger.warning(
            f"{interaction.author} (ID: {interaction.author.id}) tried to remove notifications from channel {interaction.channel_id} in guild {interaction.guild.name} (ID: {interaction.guild.id}), but the channel was not in the list.")

    elif isinstance(error, exceptions.ChannelAlreadyInList):
        """
        Used when channel is already in list
        """
        embed = disnake.Embed(
            description="That channel already is used for notifications!",
            color=0xE02B2B
        )
        await interaction.send(embed=embed)
        bot.logger.warning(
            f"{interaction.author} (ID: {interaction.author.id}) tried to add notifications to channel {interaction.channel_id} in guild {interaction.guild.name} (ID: {interaction.guild.id}), but the channel was already in the list.")
    raise error






@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id})")




# Run the bot with the token
bot.run(config["token"])
