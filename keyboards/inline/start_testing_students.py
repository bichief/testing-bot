from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def go_test(test_id):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='✅ Приступить к тестированию.',
                                                                 callback_data=f'pass_test_{test_id}')
                                        ]
                                    ])

    return keyboard