# discord_bot/search.py

import requests
from discord_bot import logging, config

API_KEY = config['GOOGLE']['API_KEY']
SEARCH_ENGINE_ID = config['GOOGLE']['SEARCH_ENGINE_ID']
BaseURL = config['GOOGLE']['CUSTOM_GOOGLE_SEARCH_URL']

class GoogleSearch:
    """ Class for searching text on google"""
    def __init__(self,keyword):
        self.keyword = keyword
        self.results = None

    def search(self,num): 
        """ Search keyword by Custom Google Search API"""
        queryparams = f"?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={self.keyword}&num={num}"
        url = BaseURL + queryparams
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                items = data.get('items')
                #logging.info(f'google search results:{items}')
                self.results = items
            else:
                logging.error(f"Google Search Response:{response}")
        except Exception as e:
            logging.error('Error occurred while searching, error:{e}')

    def get_formatted_reply(self):
        """Formatting search results"""
        items = self.results
        reply = f"Top Results\n\n"
        for item in items:
            title = item.get('title')
            snippet = item.get('snippet')
            link = item.get('link')
            formatted_item = f"Title: {title}\nDescription: {snippet}\nLink: {link}\n\n"
            reply += formatted_item  
        return reply