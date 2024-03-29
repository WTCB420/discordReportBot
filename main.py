# simple discord bot to manage user reporting on a discord server
import asyncio
import discord
import os
import yaml

# set the intents to receive messages
intents = discord.Intents.default()
intents.messages = True  # Allow the bot to send messages
intents.guilds = True  # Allows the bot to see and manage guilds (servers)
intents.members = True  # Allows the bot to handle members
intents.guild_messages = True  # Allows the bot to see messages in guilds
intents.dm_messages = True  # Allows the bot to direct message guild members
intents.message_content = True  # Allows the bot to view message content

# Bot object creation intents
bot = discord.Client(intents=intents)

# handles messages and checks if the message is the command
# I know that doesn't use discord's command registering feature, but I'm too lazy
# to learn how to use it, so I'm doing it this way
@bot.event
async def on_message(message):  # on message event
    user = message.author  # get the user who sent the message
    message.content = message.content.lower()  # convert the message to lowercase
    if message.author == bot.user or message.channel.type == discord.ChannelType.private or message.channel.id != state.get_commandChannel():  # ignore messages from bots and in dms and in the wrong channel
        return
    if message.content.startswith(f'{state.get_prefix()}{state.get_command().lower()}'):  # check if the message is the configured command
        await message.delete()  # delete the message for privacy
        if user not in state.get_currently_reporting():  # check if the user is not already reporting
            # send a message to the channel
            await message.channel.send(f'Report received. Please respond to your dms to provide further information.')
            # Start dm with the user
            await dm_start(user)
            return
        elif user in state.get_currently_reporting():  # check if the user is already reporting
            await message.channel.send(f'You already have an active report.')
            return

# This function handles the messages with the report filer
async def wait_for_message(user):
    try:
        # wait for the user to respond in dms
        message = await bot.wait_for('message', timeout=3600, check=lambda
            message: message.author == user and message.channel.type == discord.ChannelType.private)
        sanitize_input(message.content)  # sanitize the input to prevent code injection, or at least try to
        if message.attachments: # check if the message has attachments
            await user.send(f'Attachments are not supported because of bandwidth issues. If you want to send an attachment, please create a new report with {state.get_prefix()}{state.get_command()} and provide a link to the attachment.')
            return None
    except asyncio.TimeoutError:
        await user.send(f'You took too long to respond. Please create a new report with {state.get_prefix()}{state.get_command()}.')
        return None
    except Exception as e:
        await user.send(f'An error occurred. Please create a new report with {state.get_prefix()}{state.get_command()}.')
        print(e)
        return None
    if message.content.upper() == 'EXIT':
        await user.send(f'Report cancelled. Please create a new report with {state.get_prefix()}{state.get_command()}.')
        return None
    return message


# Sanitize the input to prevent code injection
# I know that this is not the best way to do it, but I kinda want to
# keep the bot simple, and it would be hilarious if someone tried to
# inject code into this shit ass bot
def sanitize_input(data):
    return data.replace('`', '').replace('*', '').replace('_', '').replace('~', '').replace('@', '')

# Initiates the dm with the user
async def dm_start(user):
    await user.send('You have created a new report. If you do not want to enter any information type "Not Needed" Type '
                    '"EXIT" to cancel the report process.')
    responses = []
    state.add_to_currently_reporting(user)  # add user to currently_reporting list, so they can't open multiple
    # reports at the same time
    for message in state.get_messages_list():  # loop through all the messages in the config
        await user.send(message)  # send the message to the user
        response = await wait_for_message(user)  # wait for the user to respond
        if response is None:  # if the user took too long to respond or cancelled the report
            state.remove_from_currently_reporting(user)  # remove the user from the currently_reporting list
            return
        responses.append(response)  # add the response to the responses list
    state.remove_from_currently_reporting(user)  # remove the user from the currently_reporting list, so they can
    # open a new report
    await user.send(f'Thank you for your report. We will review the information and take further action as necessary.')
    # send the report to the report channel
    channel = bot.get_channel(state.get_reportChannel())  # get the report channel
    alert = [f'{user.name}#{user.discriminator} has created a new report.']  # create the alert message list and
    # populate reporter information
    for message, response in zip(state.get_messages_list(), responses):  # loop through the messages and responses
        alert.append(f'{message}: {response.content}')  # add the message and response to the alert
    alert.append(f'<@&{state.get_alert_role_id()}>')  # Add the mention role from the config
    await channel.send('\n'.join(alert))  # send the alert to the report channel
    return


# This class stores the variables the must be shared between multiple functions
# I'm doing this to avoid using global variables because AI told me to
class bot_state:
    def __init__(self):
        # initialize the class variables to default values
        self.command = 'report'
        self.prefix = '!'
        self.messageTimeout = 3600
        self.reportChannel = 818260076291817521
        self.commandChannel = 818260076669566984
        self.currently_reporting = []
        self.messages_list = []
        self.role_id = 818260076291817517

    # Currently reporting list operations:
    def add_to_currently_reporting(self, user: discord.user):  # add user to currently_reporting list
        self.currently_reporting.append(user)
        return

    def remove_from_currently_reporting(self, user: discord.user):  # remove user from currently_reporting list
        self.currently_reporting.remove(user)
        return

    def get_currently_reporting(self):  # get currently_reporting list
        return self.currently_reporting

    # messages list operations:
    def add_messages_list(self, message):
        self.messages_list.append(message)
        return

    def get_messages_list(self):
        return self.messages_list

    # report channel operations:
    def set_reportChannel(self, reportChannel: int):
        self.reportChannel = reportChannel
        return

    def get_reportChannel(self):
        return self.reportChannel

    # command operations:
    def set_command(self, command: str):
        self.command = command
        return

    def get_command(self):
        return self.command

    # alert role id operations:
    def set_alert_role_id(self, role_id: int):
        self.role_id = role_id
        return

    def get_alert_role_id(self):
        return self.role_id

    # prefix operations:
    def set_prefix(self, prefix: str):
        self.prefix = prefix
        return

    def get_prefix(self):
        return self.prefix

    # message timeout operations:
    def set_messageTimeout(self, messageTimeout: int):
        self.messageTimeout = messageTimeout
        return

    def get_messageTimeout(self):
        return self.messageTimeout

    # commandChannel operations:
    def set_commandChannel(self, commandChannel: int):
        self.commandChannel = commandChannel
        return

    def get_commandChannel(self):
        return self.commandChannel

# This function loads the config from the config.yaml file
# if the file is not found or there is an error loading the file, the bot use default values
# also I know that this function is a mess and doesn't really account for a missing config file, but
# honestly I don't care, because I'm gonna be the only one using this bot.
# And you may be thinking, "I'm not you and I'm using this bot", and if that's the case, I'm sorry that
# life has brought you to this point, and I hope that things get better for you soon.
async def load_config():  # load config function
    global state
    try:
        with open('config.yaml') as f:  # config loading from config.yaml
            try:
                data = yaml.safe_load(f)  # load the yaml file
                try:
                    state.set_prefix(data['prefix'])  # get the prefix from the config
                    state.set_command(data['command'])  # get the command from the config
                    state.set_messageTimeout(data['messageTimeout'])  # get the messageTimeout from the config
                    if 'commandChannel' in data and data['commandChannel'] != 0:
                        state.set_commandChannel(data['commandChannel'])
                    else:
                        print("commandChannel not configured in config.yaml, using value that you definitely don't intend to, so that the bot doesn't break and you dont blame me.")
                    if 'reportChannel' in data and data['reportChannel'] != 0:
                        state.set_reportChannel(data['reportChannel'])  # get the reportChannel from the config
                    else:
                        print("reportChannel not configured in config.yaml, using value that you definitely don't intend to, so that the bot doesn't break and you dont blame me.")
                    if 'role_id' in data and data['role_id'] != 0:
                        # get the role_id of the role that will be mentioned in the notification
                        state.set_alert_role_id(data['role_id'])
                    else:
                        print("role_id not configured in config.yaml, using value that you definitely don't intend to, so that the bot doesn't break and you dont blame me.")
                    # loop all messages get all messages from the config
                    messages = data['messages']
                    for key, value in messages.items():  # loop through the messages
                        state.add_messages_list(value)  # add the message to the messages list
                        # print(f'{key}: {value}')
                    return
                except KeyError as e:
                    print(e)
                    print("config.yaml is missing a key, using its default value.")
                    return
            except yaml.YAMLError as e:
                print(e)  # print YAMLError if there is an error
                return
    except FileNotFoundError as e:  # catch any other exceptions
        print(e)  # print the exception
        print("config.yaml not found, using default values.")
        return

# Bot ready up handler
@bot.event
async def on_ready():  # bot starting up logic
    print('----------------------')
    print("getting config")
    await load_config()
    print("config loaded")
    print('----------------------')
    print(f'Logged in as {bot.user.name} with id {bot.user.id}')
    print('Ready for reports')
    print('----------------------')
    # set the bot's status
    await bot.change_presence(activity=discord.Game(name=f'Report with {state.get_prefix()}{state.get_command()}'))


# get the bot token from the environment variable DISCORD_BOT_TOKEN and exit if it is not set
# please for the love of god, don't hardcode the token
# if you do that, you are a bad person
# Also please pray for me, because I'm also a bad person and probably hardcoded the token
# somewhere that I forgot about, so here's hoping that whoever finds it is a good person
if os.getenv('DISCORD_BOT_TOKEN') is None:
    print("DISCORD_BOT_TOKEN is not set")
    print("Please set the DISCORD_BOT_TOKEN environment variable")
    exit(1)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
state = bot_state()  # create the bot_state object
bot.run(DISCORD_BOT_TOKEN)  # run the bot
