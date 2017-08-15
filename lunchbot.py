# https://api.slack.com/methods

import os
import time
import random
from datetime import datetime
from slackclient import SlackClient

CHANNEL = '#lunch'
BOT_NAME = 'lunchbot'
RESTAURANT_CHOICES = (('Bubble Waffle', 5), ('Close Pho', 5), ('Far Pho', 4),
                      ('McDonald\'s', 1), ('Al Basha', 1), ('Kisha Poppo', 1),
                      ('Daddy\'s Delight', 1), ('LA Chicken', 1), ('Upstairs', 0.25))

SLACK_CLIENT = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def print_bot_id(slack_user):
    api_call = SLACK_CLIENT.api_call('users.list')
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == slack_user:
                print('Bot ID for \'' + user['name'] + '\' is ' + user.get('id'))
                return user.get('id')
    else:
        print('Could not find bot user with the name ' + slack_user)

def weighted_choice(choices):
    """
    Given a list of tuples where each tuple is of the form
    (item, weight), this function will return a random choice
    taking into account the weight of each item
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w
    assert False, 'Shouldn\'t get here'

if __name__ == "__main__":
    #print_bot_id(BOT_NAME)
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    coffee_prompt = 'Coffee?'
    if SLACK_CLIENT.rtm_connect():
        print('Lunchbot connected and running!')
        while True:
            now = datetime.now()
            day = now.isoweekday()
            if (day == 2 or day == 4 and now.hour == 11 and now.minute == 5 and now.second == 0):
                restaurant = weighted_choice(RESTAURANT_CHOICES)
                lunch_prompt = 'What\'s for lunch? %s?' % restaurant
                SLACK_CLIENT.api_call('chat.postMessage', channel=CHANNEL,
                                      text=lunch_prompt, as_user=True)
            elif (day == 1 or day == 3) and (now.hour == 11 and now.minute == 30 and now.second == 0):
                # Mondays and Wednesdays
                lunch_prompt = 'Ready to go upstairs for lunch?'
                SLACK_CLIENT.api_call('chat.postMessage', channel=CHANNEL,
                                      text=lunch_prompt, as_user=True)
            if (day >= 1 and day <= 5) and (now.hour == 14 and now.minute == 30 and now.second == 0):
                SLACK_CLIENT.api_call('chat.postMessage', channel=CHANNEL,
                                      text=coffee_prompt, as_user=True)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
