from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.db_commands import get_categories


async def categories_keyboard(categories):
    keyboard = InlineKeyboardMarkup(row_width=3)

    for category in categories:
        keyboard.add(InlineKeyboardButton(text=f'❌ {category}', callback_data=f'use_{category}_true'))

    keyboard.add(InlineKeyboardButton(text=f'<< Назад', callback_data='go_test'))

    return keyboard


async def edited_categories_keyboard(category_true, lesson, ):
    keyboard = InlineKeyboardMarkup(row_width=3)
    categories = await get_categories(lesson)

    for category in categories:
        if category_true == category:
            keyboard.add(InlineKeyboardButton(text=f'✅ {category_true}', callback_data=f'use_{category}_false'))
        else:
            keyboard.add(InlineKeyboardButton(text=f'❌ {category}', callback_data=f'use_{category}_true'))
    keyboard.add(InlineKeyboardButton(text=f'Далее >>', callback_data='check'))
    keyboard.add(InlineKeyboardButton(text=f'<< Назад', callback_data='go_test'))

    return keyboard
