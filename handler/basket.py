from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto

from database.database import session, Basket, update_count_offers
from __init__ import bot, assorts
from .button import menu_basket, menu


route = Router()
assort = list(assorts.keys())

@route.callback_query(Text(startswith='basket'))
async def basket(call: CallbackQuery):
    users = [i.id_user for i in session.query(Basket.id_user).distinct()]

    if str(call.from_user.id) in users:
        price = 0

        baskets = [{'name': i.name, 'types': i.types, 'price': i.price, 'amount': i.amount} for i in session.query(Basket).filter_by(id_user=str(call.from_user.id))]
        
        name = baskets[price]['name']
        types = baskets[price]['types']
        prices = baskets[price]['price']
        amount = baskets[price]['amount']
        
        pre_photo = list(assorts.values())
        
        for i in pre_photo:
            if i['types'] == types:
                photo = FSInputFile(i['img'])
                

        prices = int(prices) * int(amount)
        caption = f"{baskets[price]['name']}\nЦЕНА {prices}"

        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

        await call.message.answer_photo(photo, 
                                caption=caption,
                                reply_markup=menu_basket(price, types, name, prices))
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        
        await call.message.answer('К сожалению у вас пока нету товаров.', reply_markup=menu())

@route.callback_query(Text(startswith="back_basket"))
async def back_basket(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) - 1

    baskets = [{'name': i.name, 'types': i.types, 'price': i.price, 'amount': i.amount} for i in session.query(Basket).filter_by(id_user=str(call.from_user.id))]

    if price < len(baskets) and price >= 0:
        name = baskets[price]['name']
        types = baskets[price]['types']
        prices = baskets[price]['price']
        amount = baskets[price]['amount']
        
        pre_photo = list(assorts.values())
        for i in pre_photo:
            if i['types'] == types:
                photo = FSInputFile(i['img'])
                
        prices = int(prices) * int(amount)
        caption = f"{baskets[price]['name']}\nЦЕНА {prices}"

        await call.message.edit_media(InputMediaPhoto(media=photo, caption=caption),
                               reply_markup=menu_basket(price, types, name, prices))

@route.callback_query(Text(startswith="next_basket"))
async def next_basket(call: CallbackQuery):
    calls = call.data.split(':')
    price = int(calls[1]) + 1

    baskets = [{'name': i.name, 'types': i.types, 'price': i.price, 'amount': i.amount} for i in session.query(Basket).filter_by(id_user=str(call.from_user.id))]

    if price < len(baskets):
        name = baskets[price]['name']
        types = baskets[price]['types']
        prices = baskets[price]['price']
        amount = baskets[price]['amount']
        
        pre_photo = list(assorts.values())

        for i in pre_photo:
            if i['types'] == types:
                photo = FSInputFile(i['img'])
                
        prices = int(prices) * int(amount)
        caption = f"{baskets[price]['name']}\nЦЕНА {prices}"

        await call.message.edit_media(InputMediaPhoto(media=photo, caption=caption),
                               reply_markup=menu_basket(price, types, name, prices))

@route.callback_query(Text(startswith="pluse_basket"))
async def pluse_basket(call: CallbackQuery):
    basket_my = call.data.split(':')

    users = [i.id_user for i in session.query(Basket.id_user).distinct()]

    types = basket_my[1]
    name = basket_my[2]
    price = basket_my[3]

    user = call.from_user

    def basket_commit(user, name, types, price):
        basket_user =  Basket(user.id, user.username, name, types, price)

        session.add(basket_user)
        session.commit()
        session.close()

    if str(user.id) in users:
        types_arr = [i.types for i in session.query(Basket).filter_by(id_user=user.id)]

        if types in types_arr:
            amount = [i.amount for i in session.query(Basket).filter_by(id_user=user.id, types=types)]

            update_count_offers(Basket.types, types, int(amount[0])+1, Basket.amount, Basket)
        else:
            basket_commit(user, name, types, price, 1)
    else:
        basket_commit(user, name, types, price, 1)
    
    await call.answer('Товар успешно добавлин в корзину', show_alert=False)
        