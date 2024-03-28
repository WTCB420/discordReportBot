# simple discord bot to manage user reporting on a discord server
import asyncio

import discord
from discord.ext import commands
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

# Bot object creation with command prefix '!' and the intents set
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_message(message):  # on message event
    user = message.author  # get the user who sent the message
    if message.author == bot.user or message.channel.type == discord.ChannelType.private:  # ignore messages from bots
        return
    if message.content.startswith(f'!{state.get_command()}'):  # check if the message is the configured command
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


async def wait_for_message(user):
    try:
        # wait for the user to respond in dms
        message = await bot.wait_for('message', timeout=3600, check=lambda
            message: message.author == user and message.channel.type == discord.ChannelType.private)
    except asyncio.TimeoutError:
        await user.send('You took too long to respond. Please create a new report with !report.')
        return None
    except Exception as e:
        await user.send('An error occurred. Please create a new report with !report.')
        print(e)
        return None
    if message.content.upper() == 'EXIT':
        await user.send('Report cancelled. Please create a new report with !report.')
        return None
    return message


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


# Class to store global variables
class bot_state:
    def __init__(self):
        self.reportChannel = 0
        self.currently_reporting = []
        self.messages_list = []
        self.command = 'report'
        self.role_id = 0

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


# DO NOT CHANGE, THIS IS USED TO LOAD THE CONFIG FILE CHANGE THE VALUES IN THE CONFIG NOT HERE
async def load_config():  # load config function
    global state
    try:
        with open('config.yaml') as f:  # config loading from config.yaml
            try:
                data = yaml.safe_load(f)  # load the yaml file
                try:
                    state.set_command(data['command'])  # get the command from the config
                    state.set_reportChannel(data['reportChannel'])  # get the reportChannel from the config
                    # get the role_id of the role that will be mentioned in the notification
                    state.set_alert_role_id(data['role_id'])
                    # loop all messages get all messages from the config
                    messages = data['messages']
                    for key, value in messages.items():
                        state.add_messages_list(value)  # add the message to the messages list
                        print(f'{key}: {value}')
                except KeyError as e:
                    print(e)
                    exit()  # abort boot because vital config is missing
            except yaml.YAMLError as e:
                print(e)  # print YAMLError if there is an error
                exit()  # abort boot because yaml error
    except FileNotFoundError as e:  # catch any other exceptions
        print(e)  # print the exception
        exit()  # abort boot because of the exception


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
    await bot.change_presence(activity=discord.Game(name='Report with !report'))


# get the bot token from the environment variable DISCORD_BOT_TOKEN and exit if it is not set
if os.getenv('DISCORD_BOT_TOKEN') is None:
    print("DISCORD_BOT_TOKEN is not set")
    print("Please set the DISCORD_BOT_TOKEN environment variable")
    exit(1)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
state = bot_state()  # create the bot_state object
bot.run(DISCORD_BOT_TOKEN)  # run the bot
