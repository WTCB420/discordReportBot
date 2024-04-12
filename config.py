import discord
import yaml

# This function loads the config from the config.yaml file
# if the file is not found or there is an error loading the file, the bot use default values
# also I know that this function is a mess and doesn't really account for a missing config file, but
# honestly I don't care, because I'm gonna be the only one using this bot.
# And you may be thinking, "I'm not you and I'm using this bot", and if that's the case, I'm sorry that
# life has brought you to this point, and I hope that things get better for you soon.
async def load():  # load config function
    state = bot_state()  # create a bot_state object
    try:
        with open('config.yaml') as f:  # config loading from config.yaml
            try:
                data = yaml.safe_load(f)  # load the yaml file
                try:
                    # moved to main.py because I need to access these variables before creating the bot object
                    # state.set_prefix(data['prefix']) # get the prefix from the config
                    # state.set_command(data['command'])  # get the command from the config
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
                        print("role_id is 0 in the config.yaml, it will not mention a role in the notification.")
                        state.set_alert_role_id(data['role_id'])
                    # loop all messages get all messages from the config
                    messages = data['messages']
                    for key, value in messages.items():  # loop through the messages
                        state.add_messages_list(value)  # add the message to the messages list
                        # print(f'{key}: {value}')
                    return state
                except KeyError as e:
                    print(e)
                    print("config.yaml is missing a key, using its default value.")
                    return state
            except yaml.YAMLError as e:
                print(e)  # print YAMLError if there is an error
                return state
    except FileNotFoundError as e:  # catch any other exceptions
        print(e)  # print the exception
        print("config.yaml not found, using default values.")
        return state


# This class is used to store variables that are used throughout the bot
# I'm doing this to avoid using global variables because AI told me to
class bot_state:
    def __init__(self):
        # initialize the class variables to default values
        self.command = 'report'
        self.messageTimeout = 3600
        self.reportChannel = 818260076291817521
        self.commandChannel = 818260076669566984
        self.currently_reporting = []
        self.messages_list = []
        self.role_id = 0
        self.prefix = '!'

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

    # prefix operations:
    def set_prefix(self, prefix: str):
        self.prefix = prefix
        return

    def get_prefix(self):
        return self.prefix

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
