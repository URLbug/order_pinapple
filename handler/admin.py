import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from __init__ import bot
from database.database import session, Admin, User


route = Router()

# Рассылка
@route.message(Command('all'))
async def all_admin(message: Message):
    arr = [i.id_user for i in session.query(Admin.id_user).distinct()]

    if str(message.from_user.id) in arr:
        for i in session.query(User.id_user).distinct():
            
            await bot.send_message(i.id_user, ' '.join(message.text.split()[1:]))
            
            await asyncio.sleep(.2)

# Отправить челу сообщение
@route.message(Command('wid'))
async def wid_admin(message: Message):
    arr = [i.id_user for i in session.query(Admin.id_user).distinct()]

    if str(message.from_user.id) in arr and message.text.split()[1].isdigit():
            await bot.send_message(message.text.split()[1], ' '.join(message.text.split()[2:]))
            
            await asyncio.sleep(1)