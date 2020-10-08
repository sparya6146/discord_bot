# discord_bot/bot.py
import os
import discord
import traceback
import json
from discord_bot import logging, config
from discord_bot.search import GoogleSearch
from discord_bot.model import History
from mongoengine.errors import NotUniqueError

## Client for handling Discord Bot
class CustomClient(discord.Client):
    async def on_ready(self):
        """Called when discord bot client is connected"""
        logging.info(f"{self.user} has connected to Discord!")

    async def on_message(self,message):
        """Called when message received by discord bot"""
        if message.author == self.user:
            return

        logging.info(f"{self.user} has got a message:{message.content}")
        message.content = message.content.lower()
        
        if message.content == 'hi':
            await message.channel.send('hey')
            return
        if message.content.startswith('!google') and message.content > '!google':
            keyword = message.content.split(' ', 1)[1]
            reply = self.google_search(keyword)
            logging.info(f'Sending Reply:{reply}')
            await message.channel.send(reply)
            return
        if message.content.startswith('!recent') and message.content > '!recent':
            keyword = message.content.split(' ', 1)[1]
            reply = self.find_recent(keyword)
            logging.info(f'Sending Reply:{reply}')
            await message.channel.send(reply)
            return

    def google_search(self,keyword):
        """ Search google with keyword and add keyword to search history """
        gs = GoogleSearch(keyword)
        result_size = config['GOOGLE']['NUM_OF_RESULTS'] if config['GOOGLE']['NUM_OF_RESULTS'] else 5
        gs.search(result_size)
        if gs.results is not None :
            # Formatting the found results
            reply = gs.get_formatted_reply()
            try:
                history = History(engine ='google',text = keyword, result = json.dumps(gs.results))
                history.save()
            except Exception as e:
                if isinstance(e,NotUniqueError):
                    logging.info(f"Duplicate search, engine: google, text: {keyword}")
                else:
                    logging.info(f'Error while saving history,error: {e}')
        else:
            logging.error('No Results Found')
            reply = 'No Results Found'
        return reply

    def find_recent(self,keyword):
        """ Find recent searches done by bot """
        recent = History.objects(text__contains=keyword)
        if len(recent)>0:
            # results found in searh history
            result=f"Recent Searches\n\n"
            for search in recent:
                result += f"{search.text}\n"
            return result
        return f"No Results Found"



