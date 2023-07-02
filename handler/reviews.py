from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.database import session, Reviews
from .button import menu_reviews, yes_or_not, menu
from .state import ReviewsState
from __init__ import bot


route = Router()

reviews_arr = []

index = 0

@route.callback_query(Text(startswith='reviews'))
async def reviews_all(call: CallbackQuery):
    reviews_all = [i.id_user for i in session.query(Reviews.id_user).distinct()] # Получает из бд id пользователей для проверки наличия отзовов в боте

    if reviews_all != []:
        reviews_arr.clear()

        for x in session.query(Reviews.id).distinct():
            id = session.query(Reviews).filter(Reviews.id == x.id)

            for i in id:
                reviews_arr.append(f'Имя: {i.name_user}\n\nОтзыв: {i.reviews}')
        
        await call.message.edit_text(reviews_arr[index], reply_markup=menu_reviews(index))
    else:
        await call.message.edit_text('К сожалению у нас пока нету отзовов', reply_markup=menu_reviews(index, False))

@route.callback_query(Text(startswith="back_reviews"))
async def back_reviews(call: CallbackQuery):
    calls = call.data.split(':')
    index = int(calls[1]) - 1

    if index <= len(reviews_arr) and index >= 0:
        types = reviews_arr[index]

        await call.message.edit_text(types, reply_markup=menu_reviews(index))

@route.callback_query(Text(startswith="next_reviews"))
async def next_reviews(call: CallbackQuery):
    calls = call.data.split(':')
    index = int(calls[1]) + 1

    if index < len(reviews_arr):
        types = reviews_arr[index]

        await call.message.edit_text(types, reply_markup=menu_reviews(index))


#### Тут мы оставляем отзыв ####

@route.callback_query(Text(startswith='send_reviews'))
async def reviews_1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Вы точно хотите оставить отзыв?', reply_markup=yes_or_not('reviews'))
    
    await state.set_state(ReviewsState.one)

@route.callback_query(ReviewsState.one, Text(startswith='yes_reviews'))
async def reviews_2(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Отлично! Тогда оставти рецензию на нашу работу <3')
    
    await state.set_state(ReviewsState.two)

@route.message(ReviewsState.two)
async def reviews_3(message: Message, state: FSMContext):
    user_data = await state.get_data()

    review = Reviews(id_user=message.from_user.id, 
                    name_user=message.from_user.username, 
                    reviews=message.text)
    
    session.add(review)
    session.commit()
    session.close()

    await state.clear()
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)

    await message.answer('Мы очень благодарны Вашему отзову! Надеямся, что Вы сможете закажите ещё у нас.', reply_markup=menu())

@route.callback_query(ReviewsState.one, Text(startswith='no_reviews'))
async def no_reviews(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text('Очень жаль. Надеямся, что Вам все понравилось и Вы сможете оставить отзыв в другой раз.', reply_markup=menu())