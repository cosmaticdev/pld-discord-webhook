# pld-discord-webhook
Remember, you can change any of this code to better fit your wants/needs, just please credit me if you plan to redistribute :)
## installation
via git:
```git clone https://github.com/cosmaticdev/pld-discord-webhook```
<br>(or you can always just copy and paste the code into a python file)

Then get the necesary packages... ``` pip install websockets discord requests ```

Then you just need to edit the first five lines of the python file and put the corresponding data
```py
minamount = 5 # minimum amount of robux for an alert to be posted 
robloxuserid = 123456 # the user id of your roblox account (shown in your roblox profile url)
discordchannelid = 12334567890123456789 # the id of the discord channel that you want the messages to be sent in
BOT_TOKEN = "sometoken" # the authentication token of your discord bot
# please make sure all data besides BOT_TOKEN are integers
```

## setting up a discord bot
- go to https://discord.com/developers/applications and log in
- create a new application (or use an existing one)
- click the Bot tab (and create one if you don't have one already)
- get the bot token and put it into the python file (this might require your 2fa code)
- click the installation tab on the left
- select guild install, discord provided link, and add the scope "bot"
- for permissions you can manually select everything you want the bot to do, but its easier to just select Administrator
- click save and copy your url
- paste it into your browser and select the server to add the bot to

## running the bot
You can run the bot through any python IDE or terminal, just make sure you have python installed. Using the IDE or terminal go to the directory the script is in and run the script (```python bot.py```, run button, etc). 
<br><br>Ideally you should get hosting for the bot if you want it on 24/7, because otherwise you might miss some donations and won't get a message, so you can either run it constantly on your pc or find some sort of cloud python hosting (there's tons of free options, perhaps replit.com?). 

## testing your setup
You can do a test by running ```<@bot> test``` in a discord channel the bot has access to (please note, this cannot check to make sure that the roblox user id is correct, you'd need to do a test pls donate donation)

## changing settings on-the-go
You don't need to change your python file to change settings, run ```<@bot> settings``` to see the settings you can change right from a discord chat (by default, anybody with administrator permissions on the server can change settings, if you want it to be only for a set of discord ID's you can change that in the code)

## need more help?
Feel free to send me a DM on discord: @cosmatic_

<br><br>
Copyright 2024 cosmatic

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
