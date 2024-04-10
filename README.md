# discordReportBot
This is a very shitty report bot that I trew together in a couple of days in my free time. Please don't actually use this. It's for a discord server that is big enough to have a report bot cause we outgrew google forms, but is not nearly big enough to invest the time or money into a making a fully featured bot that isn't a mess. Anyone's free to use it cause I really don't give a fuck, but please don't message me when it breaks. I'll probably update it for out needs.
# Prerequisite stuff
- ## Create Discord Application
I don't really wanna host this for more people than me, so you'll need to create your own discord application and use this python app to run it.
[This](https://www.geeksforgeeks.org/discord-bot-in-python/#) is a good tutorial on how to make a discord app.
- ## Enable Bot Permissions
You'll need to enable both "Server Members Intent" and "Message Content Intent" Privileged Gateway Intents in the application editor menu on the Bot subheader.
Don't forget to save your changes!
- ## Invite the bot to your server
You'll need to generate an link to invite the bot to a guild (server). For this I would recomend following the tutorial, and be absolutely certain that the bots doesn't have more permissions that it needs. This is to prevent someone from stealing your bot key and using it to destroy your server. With that said, the bot needs the following permissions:
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
```
python3 -m pip install -r requirements.txt
```
- ## Run
Ubuntu/Debian
```
DISCORD_BOT_TOKEN=(REPLACE WITH YOUR API KEY) python3 main.py
```
Windows 10/11
```
set DISCORD_BOT_TOKEN=(REPLACE WITH YOUR API KEY) && python3 main.py
```
