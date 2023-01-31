from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def groups_keyboard(groups):
    keyboard = InlineKeyboardMarkup(row_width=3)

    for group in groups:
        keyboard.add(InlineKeyboardButton(text=group, callback_data=f'group_{group}'))

    keyboard.add(InlineKeyboardButton(text='<< Назад', callback_data='go_admin'))

    return keyboard
