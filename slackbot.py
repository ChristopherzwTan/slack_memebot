#! /usr/bin/python
# 
# Lots more documentation here: 
#
# https://github.com/slackapi/python-slackclient
# https://slackapi.github.io/python-slackclient/basic_usage.html
# https://api.slack.com/methods
# 

import os
import time
import random
from slackclient import SlackClient

COMMAND = "paging"
#TODO GIVE BOT A NAME
BOT_NAME = 'luncbot'
AT_BOT = "<@" + BOT_ID +  ">"

# instantiate slack clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#slack_token = os.environ["SLACK_BOT_TOKEN"]
#slack_client = SlackClient(slack_token)

restaurants = [McDonalds, Burger King, Bubble Waffle, Pho, Sushi, Japanese, Blue Sail Cafe,
Tim Hortons
]

def which_restaurant():
    return restaurants[random.randint(len(restaurants))]

def print_bot_id(slack_user):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrive all users so we can find the bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == slack_user:
            print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else
        print("Failed to find user...")

#def respond_to_name(name="christophert"):


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        business continues as usual.
    """
    if command.lower().startswith(COMMAND):
        food = which_restaurant
        response = "Let's eat at " + food + "today!"
        #response = "Christopher's memebot at your service!"
        slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

# Main function
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Slack Bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

