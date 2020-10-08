# discord_bot/model.py
from mongoengine import *
from  datetime import datetime

# Connecting to discordbot db  
connect('discordbot')

class History(Document):
    """ Model for Search History """
    engine = StringField(required = True, max_length = 50)
    text = StringField(required=True, unique_with='engine')
    result = StringField(required = True)
    created_on = DateTimeField(required = True, default=datetime.now)

