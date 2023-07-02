from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from .button import menu_assorts
from __init__ import assorts, bot


assort = list(assorts.keys())

route = Router()

@route.callback_query(Text(startswith="assorts"))
async def assorts_start(call: CallbackQuery):
    price = 0
    
    name = assorts[assort[price]]['name']
    types = assorts[assort[price]]['types']
    prices = assorts[assort[price]]['price']
    photo = FSInputFile(assorts[assort[price]]['img'])

    caption = f"{assorts[assort[price]]['name']}\nЦЕНА {prices}\n{assorts[assort[price]]['description']}"

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await call.message.answer_photo(photo, 
                               caption=caption,
                               reply_markup=menu_assorts(price, types, name, prices))

@route.callback_query(Text(startswith="back_assort"))
async def back_assort(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) - 1

    if price < len(assort) and price >= 0:
        name = assorts[assort[price]]['name']
        types = assorts[assort[price]]['types']
        prices = assorts[assort[price]]['price']
        photo = FSInputFile(assorts[assort[price]]['img'])

        caption = f"{assorts[assort[price]]['name']}\nЦЕНА {prices}\n{assorts[assort[price]]['description']}"

        await call.message.edit_media(InputMediaPhoto(media=photo, caption=caption),
                               reply_markup=menu_assorts(price, types, name, prices))

@route.callback_query(Text(startswith="next_assort"))
async def next_assort(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) + 1

    if price < len(assort):
        name = assorts[assort[price]]['name']
        types = assorts[assort[price]]['types']
        prices = assorts[assort[price]]['price']
        photo = FSInputFile(assorts[assort[price]]['img'])

        caption = f"{assorts[assort[price]]['name']}\nЦЕНА {prices}\n{assorts[assort[price]]['description']}"

        await call.message.edit_media(InputMediaPhoto(media=photo, caption=caption),
                               reply_markup=menu_assorts(price, types, name, prices))