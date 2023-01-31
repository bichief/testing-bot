from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline.admin_menu import menu
from keyboards.inline.groups_keyboard import groups_keyboard
from loader import dp
from utils.db_api.db_commands import get_all_groups, update_tests_group


@dp.message_handler(Command('admin'))
async def admin_cmd(message: types.Message):
    await message.answer('Добро пожаловать в админ-меню!\n\n'
                         'В нем вы можете назначить тестирование определенным группам, по определенным категориям, относящимся к Вашей дисциплине.', reply_markup=menu)


@dp.callback_query_handler(Text(equals='go_admin'))
async def admin_call(call: types.CallbackQuery):
    await call.message.edit_text('Добро пожаловать в админ-меню!\n\n'
                                 'В нем вы можете назначить тестирование определенным группам, по определенным категориям, относящимся к Вашей дисциплине.', reply_markup=menu)


@dp.callback_query_handler(Text(equals='go_test'))
async def select_current_group(call: types.CallbackQuery):
    groups = await get_all_groups()
    keyboard = await groups_keyboard(groups=groups)

    await call.message.edit_text('Выберите необходимую для тестирования группу:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='group'))
async def get_admin_group(call: types.CallbackQuery):
    group = call.data.split('_')[1]
    await update_tests_group(group=group, telegram_id=call.from_user.id)

    await call.message.edit_text('None')
