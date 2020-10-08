# discord_bot/__init__.py

import configparser
import logging

# loading config
config = configparser.ConfigParser()
config.read('instance/config.py')

# logging configuration
logging.basicConfig(filename='console.log', level=logging.INFO)

logging.info('Session Start')

from discord_bot.bot import CustomClient

# Token for Discord Bot Connection
TOKEN = config['DISCORD']['DISCORD_TOKEN']

def start_bot():
    logging.info('Starting Discord Bot....')
    client = CustomClient()
    client.run(TOKEN)