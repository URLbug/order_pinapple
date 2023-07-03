from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .state import Order
from .button import yes_or_not, menu
from database.database import User_2, Admin, session
from __init__ import bot


route = Router()

order_me = {}

@route.callback_query(Text(startswith='order'))
async def user_order(call: CallbackQuery, state: FSMContext):
    calls = call.data.split(':')

    order_me['id_user'] = call.from_user.id
    order_me['user_name'] = call.from_user.username
    order_me['type'] = calls[1]
    order_me['name'] = calls[2]
    order_me['price'] = calls[3]

    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    await call.message.answer('Вы точно хотите заказать этот заказ?', reply_markup=yes_or_not('order'))
    await state.set_state(Order.one)

@route.callback_query(Order.one, Text(startswith="yes_order"))
async def user_order_2(call: CallbackQuery, state: FSMContext):
    await state.update_data(one=call.message.text)

    await call.message.edit_text('Напишит Ваши пожелание к доставке.')
    await state.set_state(Order.two)

@route.message(Order.two)
async def user_order_3(message: Message, state: FSMContext):
    user_data = await state.get_data()
    
    order_me['description'] = message.text

    users = User_2(id_user=order_me['id_user'], name_user=order_me['user_name'], types=order_me['type'], description=order_me['description'])

    session.add(users)
    session.commit()
    session.close()
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

    await state.clear()
    await message.answer('Отлично! Ожидайте ответа от нашего менеджера.', reply_markup=menu())

    text = f'Поступил новый заказ от {order_me["user_name"]}({order_me["id_user"]})\n\nОписание и наименование заказа:\n{order_me["type"]} {order_me["name"]} {order_me["price"]}\n{order_me["description"]}'

    for i in session.query(Admin.id_user).distinct():
        try:
            await bot.send_message(i.id_user, text)
        except:
            print(f'Not activiti {i.id_user}')
    
    order_me.clear()

@route.callback_query(Order.one, Text(startswith="no_order"))
async def user_order_4(call: CallbackQuery, state: FSMContext):
    order_me.clear()

    await state.clear()
    await call.message.edit_text('Если вам не понравился этот товар, тогда Вы можете посмотреть друге товары которые мы предоставляем.', reply_markup=menu())