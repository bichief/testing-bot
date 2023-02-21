from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def testing_kb(list_id):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='Приступить',
                                                                 callback_data=f'pre_start_{list_id}_o')
                                        ]
                                    ])
    return keyboard
