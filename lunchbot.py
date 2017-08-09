# https://api.slack.com/methods

import os
import time
from datetime import datetime
from slackclient import SlackClient

channel='#lunch'
BOT_NAME = 'lunchbot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def print_bot_id(slack_user):
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == slack_user:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                return user.get('id')
    else:
        print("could not find bot user with the name " + slack_user)
    
        
if __name__ == "__main__":
    #print_bot_id(BOT_NAME)
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    lunch_prompt="What's for lunch?"
    coffee_prompt="Coffee?"
    if slack_client.rtm_connect():
        print("Lunchbot connected and running!")
        while True:
            now = datetime.now()
            day = now.isoweekday()
            if (day == 2 or day == 4) and (now.hour == 11 and now.minute == 25 and now.second == 0):
                slack_client.api_call("chat.postMessage", channel=channel,
                          text=lunch_prompt, as_user=True)
            if (now.hour == 14 and now.minute == 30 and now.second == 0):
                slack_client.api_call("chat.postMessage", channel=channel,
                          text=coffee_prompt, as_user=True)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
    
