# https://api.slack.com/methods

import os
import time
import random
import json
from datetime import datetime
from slackclient import SlackClient

class Lunchbot(object):
    """
    Lunchbot is a Slack bot
    """

    # Slack constants
    CHANNEL = '#lunch'
    BOT_NAME = 'lunchbot'
    SLACK_CLIENT = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
    READ_WEBSOCKET_DELAY = 60 # 1 minute delay between reading from firehose

    # Lunchbot constants
    RESTAURANTS = {}
    MESSAGES = {}

    def __init__(self):
        self.read_data()

    def read_data(self):
        """
        Reads data from data file and updates internal constants
        """
        with open('data.json') as data_file:
            data = json.load(data_file)
        self.RESTAURANTS = data['restaurants']
        self.MESSAGES = data['messages']

    def print_bot_id(self, slack_user):
        """
        Prints ID of given user
        """
        api_call = self.SLACK_CLIENT.api_call('users.list')
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == slack_user:
                    print 'Bot ID for \'' + user['name'] + '\' is ' + user.get('id')
                    return user.get('id')
        else:
            print 'Could not find bot user with the name ' + slack_user

    def weighted_choice(self, choices):
        """
        Given a list of tuples where each tuple is of the form
        (item, weight), this function will return a random choice
        taking into account the weight of each item
        """
        # total = sum(w for c, w in choices)
        total = sum(item['weight'] for item in choices)
        r = random.uniform(0, total)
        upto = 0
        for item in choices:
            if upto + item['weight'] >= r:
                return item['name']
            upto += item['weight']
        assert False, 'Shouldn\'t get here'

    def run(self):
        """
        Main loop/logic of lunchbot
        """
        if self.SLACK_CLIENT.rtm_connect():
            print 'Lunchbot connected and running!'
            while True:
                now = datetime.now()
                current_time = now.strftime('%H:%M')
                day = now.strftime('%A')

                for message in self.MESSAGES:
                    if current_time == message['time'] and day in message['days']:
                        msg = message['message']

                        # Append restaurant when eating out
                        if message['type'] == 'eating_out':
                            msg = '%s %s?' % (msg, self.weighted_choice(self.RESTAURANTS))

                        self.SLACK_CLIENT.api_call('chat.postMessage', channel=self.CHANNEL,
                                                   text=msg, as_user=True)

                time.sleep(self.READ_WEBSOCKET_DELAY)
        else:
            print 'Connection failed. Invalid Slack token or bot ID?'


if __name__ == "__main__":
    BOT = Lunchbot()
    # BOT.print_bot_id(BOT.BOT_NAME)

    BOT.run()
