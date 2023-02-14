from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_final_menu = InlineKeyboardMarkup(row_width=3,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Начать тестирование',
                                                                     callback_data='start_test')
                                            ],
                                            [
                                                InlineKeyboardButton(text='<< Назад', callback_data='go_test')
                                            ]
                                        ])
