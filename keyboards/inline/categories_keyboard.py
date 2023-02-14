from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_categories, get_category_id


async def categories_keyboard(lesson):
    keyboard = InlineKeyboardMarkup(row_width=3)
    categories = await get_categories(lesson)
    for i in range(len(categories)):
        keyboard.add(
            InlineKeyboardButton(text=f'{categories[i].category_name}', callback_data=f'use_{categories[i].id}_true'))

    keyboard.add(InlineKeyboardButton(text=f'<< Назад', callback_data='go_test'))

    return keyboard


async def edited_categories_keyboard(category_true, lesson, ):
    keyboard = InlineKeyboardMarkup(row_width=3)
    categories = await get_categories(lesson)

    for i in range(len(categories)):
        keyboard.add(
            InlineKeyboardButton(text=f'{categories[i].category_name}', callback_data=f'use_{categories[i].id}_true'))
    keyboard.add(InlineKeyboardButton(text=f'Далее >>', callback_data='check'))
    keyboard.add(InlineKeyboardButton(text=f'<< Назад', callback_data='go_test'))

    return keyboard
