#! /usr/bin/python

import os
from slackclient import SlackClient

#TODO GIVE BOT A NAME
BOT_NAME = ''

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#slack_token = os.environ["SLACK_BOT_TOKEN"]
#slack_client = SlackClient(slack_token)


def print_bot_info(slack_user):
    if __name == "__main__":
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrive all users so we can find the bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == slack_user:
                    print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
        else
            print("Failed to find user...")


