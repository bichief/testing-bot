from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def exam_kb(list_id):
    keyboard = InlineKeyboardMarkup(row_width=3,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text='1.', callback_data=f'pre_start_{list_id + 1}_1')
                                        ],
                                        [
                                            InlineKeyboardButton(text='2.', callback_data=f'pre_start_{list_id + 1}_2')
                                        ],
                                        [
                                            InlineKeyboardButton(text='3.', callback_data=f'pre_start_{list_id + 1}_3')
                                        ]
                                    ])

    return keyboard
