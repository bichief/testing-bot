from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def lesson_keyboard(lessons):
    keyboard = InlineKeyboardMarkup(row_width=3)

    for lesson in lessons:
        keyboard.add(InlineKeyboardButton(text=lesson, callback_data=f'lesson_{lesson}'))

    keyboard.add(InlineKeyboardButton(text='<< Назад', callback_data='go_test'))
    return keyboard
