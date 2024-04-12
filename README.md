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
![firefox_VqgEdnUTdl](https://github.com/WTCB420/discordReportBot/assets/36096475/d07b386a-41c3-4cd9-963a-50d655743dec)
![firefox_DulRGZzQ69](https://github.com/WTCB420/discordReportBot/assets/36096475/3b10283a-574c-4136-863d-27a0123f8a05)

### Note: You will need to manually give the bot permissions to the channels you want it to look for the command in and where you want it to output the completed reports. It also needs permissions to send notification to the role you wish. 

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
This key defines where the bot should listen for the command. This needs to be a number (integer). E.g., 800836208007446528 could point to #bot-stuff. Leaving this at zero will use default values and may break the bot.
### Note: You can find the ID of the channels or groups with [this](https://docs.statbot.net/docs/faq/general/how-find-id/) tutorial.
```
commandChannel: 0
```
This key defines where the bot should post the information provided in a completed report. This needs to be a number (integer). E.g. 818260076291817521 could point to #completed-reports.  Leaving this at zero will use default values and may break the bot.
```
reportChannel: 0
```
This key handles what role the bot should mention when a report is completed. E.g. 1227702564880126114 could be for @admin. Leaving at 0 will disable mentions.
```
role_id: 0
```
This is the amount of time, in seconds, the bot should wait before ending an inactive report instance. 3600 seconds = 1 hour 
```
messageTimeout: 3600
```
This section contains the messages that will be sent to the person who opens a report. It will send all the messages under the 'messages' parent key, no matter their key (as long as they follow json syntax and have a unique key).
```
messages:
  username: "What is the username of the person who you are reporting?"
  issueMessage: "Being as detailed as possible, what issue are you facing?"
  userSolvedStateMessage: "How would you like the issue to be resolved?"
  reachOutMessage: "Would you like us to contact you for further information?"
```
If you wanted, for example, to add an option to ask the user what rule they think the offender broke, you could add the following.
```
messages:
  username: "What is the username of the person who you are reporting?"
  issueMessage: "Being as detailed as possible, what issue are you facing?"
  ruleBrokenMessage: "What rule do you think they broke?"
  userSolvedStateMessage: "How would you like the issue to be resolved?"
  reachOutMessage: "Would you like us to contact you for further information?"
```


And that about wraps up everything to configure. If you have any questions, feel free to reach out, bearing in mind that I'm not a professional dev and this is a free bot. 
