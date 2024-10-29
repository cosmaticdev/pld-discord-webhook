minamount = 0
maxlength = 999
robloxuserid = YOUR ROBLOX USER
discordchannelid = YOUR CHANNEL ID
BOT_TOKEN = "YOUR TOKEN"

import asyncio, websockets
import discord
from discord.ext import commands, tasks
import time, os, requests, json, threading
from pathlib import Path


async def connect_to_websocket():
    uri = f"wss://stream.plsdonate.com/api/user/{robloxuserid}/websocket"
    async with websockets.connect(uri) as websocket:
        # Send a message
        await websocket.send(f"Hello from {robloxuserid}!")
        print("Connected to websocket")

        # Receive a message
        while True:
            response = await websocket.recv()
            """ {"message":str,"sender":{"id":int,"username":str,"displayName":str},"amount":int} """
            print("Message received from server:", response)
            print(type(response))
            await sendMessage(response)


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
                    "maxlength": maxlength,
                    "channelid": discordchannelid,
                    "robloxuserid": robloxuserid,
                }
            )
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")


@bot.event
async def on_message(message):
    if message.author.guild_permissions.administrator:
        if message.content.startswith(f"<@{bot.user.id}> settings"):
            if message.content.split(f"<@{bot.user.id}> settings ")[1].split(" ")[
                0
            ].lower() in ["minamount", "maxlength", "channelid", "robloxuserid"]:

                try:
                    int(
                        (
                            message.content.split(f"<@{bot.user.id}> settings ")[
                                1
                            ].split(" ")[1]
                        )
                    )
                except:
                    await message.channel.send(
                        "Please only send an int value for your data",
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

                await message.channel.send(
                    "Updated your settings",
                    reference=message,
                )
                return
            else:
                await message.channel.send(
                    f"That's not a valid setting, run '<@{bot.user.id}> help' to see what is.",
                    reference=message,
                )
                return
        elif message.content.startswith(f"<@{bot.user.id}>"):

            await message.channel.send(
                f"Configure settings:\n'<@{bot.user.id}> settings <setting> <value>'\noptions: minamount, maxlength, channelid, robloxuserid",
                reference=message,
            )
            return


async def sendMessage(data):
    print(type(data))
    data = json.loads(data)
    try:
        with open("settings.json") as f:
            temp = json.loads(f.read())

        channel = bot.get_channel(temp["channelid"])
        if channel is not None:
            message = f"{data['sender']['displayName']} ({data['sender']['username']}) sent {data['amount']} robux via pls donate!\n{data['message']}"
            print(message)
            await channel.send(message)
        else:
            print("Channel not found.")
    except Exception as e:
        print(e.message)


async def main():

    task = asyncio.create_task(connect_to_websocket())

    await bot.start(BOT_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
        asyncio.create_task(main())
    except RuntimeError:
        asyncio.run(main())
