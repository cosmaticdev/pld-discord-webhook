minamount = 0
robloxuserid = YOUR ROBLOX USER
discordchannelid = YOUR CHANNEL ID
BOT_TOKEN = "YOUR TOKEN"
# make sure all data (besides BOT_TOKEN are integers!)

import asyncio, websockets
import discord
from discord.ext import commands, tasks
import time, os, requests, json, threading
from pathlib import Path


async def connect_to_websocket():
    try:
        with open("settings.json") as f:
            temp = json.loads(f.read())

        uri = f"wss://stream.plsdonate.com/api/user/{temp['robloxuserid']}/websocket"
        async with websockets.connect(uri) as websocket:
            # Send a message
            await websocket.send(f"Hello from {temp['robloxuserid']}!")
            print(f"Connected to websocket as {temp['robloxuserid']}")

            # Receive a message
            while True:
                response = await websocket.recv()
                """ {"message":str,"sender":{"id":int,"username":str,"displayName":str},"amount":int} """
                print("Message received from server:", response)
                response = json.loads(response)
                if response["amount"] >= temp["minamount"]:
                    await sendMessage(response)
                else:
                    print(f"Last donation was too small! ({response['amount']})")
    except asyncio.CancelledError:
        print("Websocket needs reconnection")


intents = discord.Intents.default()  # set intents
intents.messages = True

bot = commands.Bot(command_prefix="", intents=intents)

my_file = Path("settings.json")
if not my_file.is_file():
    with open("settings.json", "w") as f:
        f.write(
            json.dumps(
                {
                    "minamount": minamount,
                    "channelid": discordchannelid,
                    "robloxuserid": robloxuserid,
                }
            )
        )


@bot.event
async def on_ready():
    print(f"Logged in to discord as {bot.user.name} ({bot.user.id})")


@bot.event
async def on_message(message):
    if message.author.guild_permissions.administrator:
        if message.content.startswith(f"<@{bot.user.id}> settings "):
            if message.content.split(f"<@{bot.user.id}> settings ")[1].split(" ")[
                0
            ].lower() in ["minamount", "channelid", "robloxuserid"]:

                try:
                    int(
                        (
                            message.content.split(f"<@{bot.user.id}> settings ")[
                                1
                            ].split(" ")[1]
                        )
                    )
                except:
                    embed = discord.Embed(
                        title="Whoops!",
                        description="Please only send an int value for your data",
                        color=discord.Color.purple(),
                    )
                    await message.channel.send(
                        embed=embed,
                        reference=message,
                    )
                    return

                with open("settings.json") as f:
                    data = json.loads(f.read())
                data[
                    message.content.split(f"<@{bot.user.id}> settings ")[1]
                    .split(" ")[0]
                    .lower()
                ] = int(
                    message.content.split(f"<@{bot.user.id}> settings ")[1]
                    .split(" ")[1]
                    .lower()
                )
                with open("settings.json", "w") as f:
                    f.write(json.dumps(data, indent=2))

                embed = discord.Embed(
                    title="Updated!",
                    description=f'Updated your {message.content.split(f"<@{bot.user.id}> settings ")[1].split(" ")[0].lower()} setting!',
                    color=discord.Color.purple(),
                )

                await message.channel.send(
                    embed=embed,
                    reference=message,
                )

                if (
                    message.content.split(f"<@{bot.user.id}> settings ")[1]
                    .split(" ")[0]
                    .lower()
                    == "robloxuserid"
                ):
                    global task

                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        print("Task cancelled.")

                    task = asyncio.create_task(connect_to_websocket())

                return
            else:
                embed = discord.Embed(
                    title="Whoops!",
                    description=f"That's not a valid setting, run '<@{bot.user.id}> help' to see what is.",
                    color=discord.Color.purple(),
                )
                await message.channel.send(
                    embed=embed,
                    reference=message,
                )
                return

        elif message.content.startswith(f"<@{bot.user.id}> test"):
            embed = discord.Embed(
                title="Running Test",
                description="Running a test donation! Go check if it's in the right channel!",
                color=discord.Color.purple(),
            )
            await message.channel.send(
                embed=embed,
                reference=message,
            )
            await sendMessage(
                {
                    "message": "This is a test donation!",
                    "sender": {
                        "id": "NA",
                        "username": "radcaterator",
                        "displayName": "cosmatic",
                    },
                    "amount": 10000000,
                }
            )

            return

        elif message.content.startswith(f"<@{bot.user.id}>"):

            embed = discord.Embed(
                title="Settings",
                description=f"Configure settings:\n'<@{bot.user.id}> settings <setting> <value>'\noptions: minamount, channelid, robloxuserid\nRun a test donation using '<@{bot.user.id}> test'",
                color=discord.Color.purple(),
            )

            await message.channel.send(
                embed=embed,
                reference=message,
            )
            return


async def sendMessage(data):
    try:
        with open("settings.json") as f:
            temp = json.loads(f.read())

        channel = bot.get_channel(temp["channelid"])
        if channel is not None:
            message = f"{data['sender']['displayName']} ({data['sender']['username']}) sent {data['amount']} robux via pls donate!\n\"{data['message']}\""
            embed = discord.Embed(
                title="New tip!",
                description=message,
                color=discord.Color.purple(),
            )
            print(message)
            await channel.send(embed=embed)
        else:
            print("Channel not found.")
    except Exception as e:
        print(e.message)


async def main():
    global task
    task = asyncio.create_task(connect_to_websocket())

    await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
        asyncio.create_task(main())
    except RuntimeError:
        asyncio.run(main())
