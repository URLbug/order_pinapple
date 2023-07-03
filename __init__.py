import json

from aiogram import Bot

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


config = json.load(open('./jsons/config.json', 'rb'))
admins = json.load(open('./jsons/admin.json', 'rb'))
assorts = json.load(open('./jsons/assorts.json', 'rb'))

bot = Bot(config['TOKEN'])

engine = create_engine(config['DATABASE'])

Base = declarative_base()
metadata_obj = MetaData()