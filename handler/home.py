from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text

from database.database import session, User
from .button import menu
from __init__ import bot

route = Router()

@route.message(Command('start'))
async def home(message: Message):
    user_all = [i.id_user for i in session.query(User.id_user).distinct()] # Получает из бд id пользователей 
    user = message.from_user 

    # Проверка зареган пользователей в бд, либо нет
    if str(user.id) not in user_all:
        users = User(str(user.id), user.username)
        session.add(users)
        session.commit()
        session.close()

    await message.answer("ПРОДАЮ В АРЕНДУ СОЧНЫЕ, СПЕЛЫЕ ДЫНИ!!!!!!!", reply_markup=menu())

@route.callback_query(Text(startswith='main_menu'))
async def main_menu(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    
    await call.message.answer("ПРОДАЮ В АРЕНДУ СОЧНЫЕ, СПЕЛЫЕ ДЫНИ!!!!!!!", reply_markup=menu())
