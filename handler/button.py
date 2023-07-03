from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu():
    build = InlineKeyboardBuilder()

    build.button(text='Ассортимент', callback_data='assorts')
    build.button(text='Отзывы', callback_data='reviews')
    build.button(text='Корзина', callback_data='basket')

    build.adjust(2)

    return build.as_markup()

def yes_or_not(handler):
    build = InlineKeyboardBuilder()

    build.button(text='Да', callback_data=f'yes_{handler}')
    build.button(text='Нет', callback_data=f'no_{handler}')

    build.adjust(2)

    return build.as_markup(resize_keyboard=True)

def menu_reviews(price, pluse=True):
    build = InlineKeyboardBuilder()

    if pluse:
        build.button(text="<", callback_data=f"back_reviews:{price}")
        build.button(text=str(price+1), callback_data="null")
        build.button(text=">", callback_data=f"next_reviews:{price}")
    
    build.button(text="Оставить отзыв", callback_data=f"send_reviews")
    build.button(text="Главное меню", callback_data="main_menu")

    build.adjust(3)

    return build.as_markup()

def menu_assorts(price, types, name, prices):
    build = InlineKeyboardBuilder()

    build.button(text="<", callback_data=f"back_assort:{price}")
    build.button(text=str(price+1), callback_data="null")
    build.button(text=">", callback_data=f"next_assort:{price}")
    build.button(text="Заказать", callback_data=f"order:{types}:{name}:{prices}")
    build.button(text="Добавть в корзину", callback_data=f"pluse_basket:{types}:{name}:{prices}")
    build.button(text="Главное меню", callback_data="main_menu")

    build.adjust(3)

    return build.as_markup()

def menu_basket(price, types, name, prices):
    build = InlineKeyboardBuilder()

    build.button(text="<", callback_data=f"back_basket:{price}")
    build.button(text=str(price+1), callback_data="null")
    build.button(text=">", callback_data=f"next_basket:{price}")
    build.button(text="Заказать", callback_data=f"order:{types}:{name}:{prices}")
    build.button(text="Главное меню", callback_data="main_menu")

    build.adjust(3)

    return build.as_markup()