# discordReportBot
This is a very shitty report bot that I threw together in a couple of days of my free time. Please don't actually use this. It's for a Discord server that is big enough to have a report bot because we outgrew Google Forms, but is not nearly big enough to invest the time or money into making a fully featured bot that isn't a mess. Anyone's free to use it because I really don't give a fuck, but please don't message me when it breaks. I'll probably update it for our needs.
# Prerequisite stuff
- ## Create Discord Application
I don't really want to host this for more people than me, so you'll need to create your own Discord application and use this python app to run it.
[This](https://www.geeksforgeeks.org/discord-bot-in-python/#) is a good tutorial on how to make a discord app.
- ## Enable Bot Permissions
You'll need to enable both "Server Members Intent" and "Message Content Intent" Privileged Gateway Intents in the application editor menu on the Bot subheader.
Don't forget to save your changes!
- ## Invite the bot to your server
You'll need to generate a link to invite the bot to a guild (server). For this, I would recommend following the tutorial and being absolutely certain that the bot doesn't have more permissions than it needs. This is to prevent someone from stealing your bot key and using it to destroy your server. With that said, the bot needs the following permissions:
- Bot
- Messages
- guilds
- members
- guild.members
- dm_messages
- message_content
# Install
- ## Get programs
-Ubuntu/Debian
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip git 
```
-Windows 10/11 [Chocholatey](https://chocolatey.org/install)

Open an Administrator Command Prompt
```
choco install python3 git
```
- ## Clone Repository
```
git clone https://github.com/WTCB420/discordReportBot.git
cd discordReportBot
```
- ## Install Requirements

### Note: while not strictly nessicary, it is advisable to create a virtual enviorment to install all packages. See [this](https://docs.python.org/3/library/venv.html) reference for more information on setting one up.
```
python3 -m pip install -r requirements.txt
```
- ## Create and populate .env file
Ubuntu/Debian
```
nano .env
```
Add the following text to the file, removing the (ENTER TOKEN HERE) with your actual token.
```
DISCORD_BOT_TOKEN = "(ENTER TOKEN HERE)"
```
Press CTRL + O then RETURN then CTRL + X
Windows 10/11
```
notepad.exe .env
```
Add the following text to the file, removing the (ENTER TOKEN HERE) with your actual token.
```
DISCORD_BOT_TOKEN = "(ENTER TOKEN HERE)"
```
Press CTRL + S and close the file 

- ## Run
### Note: If you chose to set up a virtual environment, you will need to replace python3 with the path to the local python executable. E.g. ~/venv/Scripts/python3.exe 
```
python3 main.py
```
# Configure
This is the part where you change the default config.yaml so the bot will function properly. 

This is the key that is entered before the report command. Eg. !report where the ! is the prefix
```
prefix: "!"
```
This key defines what word following the prefix will trigger the bot's logic. E.g. !report, where report is the command
```
command: "report"
```
This key defines where the bot should listen for the command. This needs to be a number (integer). E.g., 800836208007446528 goes to #bot-stuff. Leaving this at zero will use default values and may break the bot.
### Note: You can find the ID of the channels or groups with [this](https://docs.statbot.net/docs/faq/general/how-find-id/) tutorial.
And that about wraps up everything to configure. If you have any questions, feel free to reach out, bearing in mind that I'm not a professional dev and this is a free bot. 
