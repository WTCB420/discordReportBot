import asyncio
import discord


# This function handles the messages with the report filer
async def wait_for_message(user, bot, state, prefix):
    try:
        # wait for the user to respond in dms
        message = await bot.wait_for('message', timeout=3600, check=lambda
            message: message.author == user and message.channel.type == discord.ChannelType.private)
        sanitize_input(message.content)  # sanitize the input to prevent code injection, or at least try to
        if message.attachments:  # check if the message has attachments
            attachment_urls = [attachment.url for attachment in message.attachments]  # get the urls of the attachments
            message.content += '\n'.join(attachment_urls)  # add the urls to the message content
    except asyncio.TimeoutError:
        await user.send(f'You took too long to respond. Please create a new report with {prefix}{state.get_command()}.')
        return None
    except Exception as e:
        await user.send(f'An error occurred. Please create a new report with {prefix}{state.get_command()}.')
        print(e)
        return None
    if message.content.upper() == 'EXIT':
        await user.send(f'Report cancelled. Please create a new report with {prefix}{state.get_command()}.')
        return None
    return message


# Initiates the dm with the user
async def dm_start(user, bot, state, prefix):
    await user.send('You have created a new report. If you do not want to enter any information type "Not Needed" Type '
                    '"EXIT" to cancel the report process.')
    responses = []
    state.add_to_currently_reporting(user)  # add user to currently_reporting list, so they can't open multiple
    # reports at the same time
    for message in state.get_messages_list():  # loop through all the messages in the config
        await user.send(message)  # send the message to the user
        response = await wait_for_message(user, bot, state, prefix)  # wait for the user to respond
        if response is None:  # if the user took too long to respond or cancelled the report
            state.remove_from_currently_reporting(user)  # remove the user from the currently_reporting list
            return
        responses.append(response)  # add the response to the responses list
    state.remove_from_currently_reporting(user)  # remove the user from the currently_reporting list, so they can
    # open a new report
    await user.send(f'Thank you for your report. We will review the information and take further action as necessary.')
    # send the report to the report channel
    channel = bot.get_channel(state.get_reportChannel())  # get the report channel
    alert = [f'{user.name} has created a new report.']  # create the alert message list and
    # populate reporter information
    for message, response in zip(state.get_messages_list(), responses):  # loop through the messages and responses
        alert.append(f'{message}: {response.content}')  # add the message and response to the alert
    if state.get_alert_role_id() != 0:
        alert.append(f'<@&{state.get_alert_role_id()}>')  # Add the mention role from the config
    await channel.send('\n'.join(alert))  # send the alert to the report channel
    return


# Sanitize the input to prevent code injection
# I know that this is not the best way to do it, but I kinda want to
# keep the bot simple, and it would be hilarious if someone tried to
# inject code into this shit ass bot
def sanitize_input(data):
    return data.replace('`', '').replace('*', '').replace('_', '').replace('~', '').replace('@', '')
