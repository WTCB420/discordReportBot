# simple discord bot to manage user reporting on a discord server
import discord
import os
import yaml
from discord.ext.commands import Bot

from config import load
from messaging import dm_start
from dotenv import load_dotenv, dotenv_values

# set the intents to receive messages
intents = discord.Intents.default()
intents.messages = True  # Allow the bot to send messages
intents.guilds = True  # Allows the bot to see and manage guilds (servers)
intents.members = True  # Allows the bot to handle members
intents.guild_messages = True  # Allows the bot to see messages in guilds
intents.dm_messages = True  # Allows the bot to direct message guild members
intents.message_content = True  # Allows the bot to view message content

# get the prefix and command from the config
try:
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
        prefix = config['prefix']
        command = config['command']
except FileNotFoundError:
    print("config.yaml not found, using default values.")
    prefix = '!'
    command = 'report'
except KeyError:
    print("Either prefix or command is missing from config.yaml, using default values for both.")
    prefix = '!'
    command = 'report'


# Bot object creation with prefix and intents
bot = Bot(command_prefix=prefix, intents=intents)

# handles the command to create a new report
@bot.command(name=command)
async def report(command):  # report command
    user = command.author  # get the user who sent the command
    if command.author == bot.user or command.channel.type == discord.ChannelType.private or command.channel.id != state.get_commandChannel():  # ignore commands from bots and in dms and in the wrong channel
        return
    await command.message.delete()  # delete the command for privacy
    if user not in state.get_currently_reporting():  # check if the user is not already reporting
        # send a command to the channel
        await command.channel.send(f'Report received. Please respond to your dms to provide further information.')
        # Start dm with the user
        await dm_start(user, bot, state, prefix)
        return
    elif user in state.get_currently_reporting():  # check if the user is already reporting
        await command.channel.send(f'You already have an active report.')
        return

# Bot ready up handler
@bot.event
async def on_ready():  # bot starting up logic
    print('----------------------')
    print('Getting config')
    global state
    state = await load()  # load the config
    print('Config loaded')
    print('----------------------')
    print(f'Logged in as {bot.user.name} with id {bot.user.id}')
    print('Ready for reports')
    print('----------------------')
    # set the bot's status
    await bot.change_presence(activity=discord.Game(name=f'Report with {prefix}{state.get_command()}'))


# get the bot token from the environment variable DISCORD_BOT_TOKEN and exit if it is not set
# please for the love of god, don't hardcode the token
# if you do that, you are a bad person
# Also please pray for me, because I'm also a bad person and probably hardcoded the token
# somewhere that I forgot about, so here's hoping that whoever finds it is a good person
try:
    load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
except KeyError:
    print("DISCORD_BOT_TOKEN is not set")
    print("Please set the DISCORD_BOT_TOKEN environment variable")
    exit(1)

bot.run(DISCORD_BOT_TOKEN)  # run the bot
