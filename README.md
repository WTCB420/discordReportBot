# discordReportBot
This is a very shitty report bot that I trew together in a couple of days in my free time. Please don't actually use this. It's for a discord server that is big enough to have a report bot cause we outgrew google forms, but is not nearly big enough to invest the time or money into a making a fully featured bot that isn't a mess. Anyone's free to use it cause I really don't give a fuck, but please don't message me when it breaks. I'll probably update it for out needs.
# Prerequisite stuff
- ## Create Discord Application
I don't really wanna host this for more people than me, so you'll need to create your own discord application and use this python app to run it.
[This](https://www.geeksforgeeks.org/discord-bot-in-python/#) is a good tutorial on how to make a discord app.
# Install
- ## Get programs
-Ubuntu/Debian
```
sudo apt-get update
sudo apt-get install -y python3 python3-pip git 
```
-Windows 10 [Chocholatey](https://chocolatey.org/install)
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
- ## Create .env file with DISCORD_BOT_TOKEN
-Ubuntu/Debian
```
nano .env
```
Enter enviormental variable
```
DISCORD_BOT_TOKEN=(INSERT YOUR TOKEN HERE)
```
Press Ctrl + O then ENTER then CTRL X
-Windows 10
```
notepad .env
```

- ## Run
```
python3
