from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline.admin_final import admin_final_menu
from keyboards.inline.admin_menu import menu
from keyboards.inline.categories_keyboard import categories_keyboard, edited_categories_keyboard
from keyboards.inline.groups_keyboard import groups_keyboard
from keyboards.inline.lessons_keyboard import lesson_keyboard
from loader import dp
from utils.db_api.db_commands import get_all_groups, update_tests_group, get_lessons, update_tests_lesson, \
    get_categories, update_category, get_categories_test, delete_test_row, get_test_teacher_id


@dp.message_handler(Command('admin'))
async def admin_cmd(message: types.Message):
    await message.answer('Добро пожаловать в админ-меню!\n\n'
                         'В нем вы можете назначить тестирование определенным группам, по определенным категориям, '
                         'относящимся к Вашей дисциплине.', reply_markup=menu)


@dp.callback_query_handler(Text(equals='go_admin'))
async def admin_call(call: types.CallbackQuery):
    await call.message.edit_text('Добро пожаловать в админ-меню!\n\n'
                                 'В нем вы можете назначить тестирование определенным группам, по определенным '
                                 'категориям, относящимся к Вашей дисциплине.', reply_markup=menu)


@dp.callback_query_handler(Text(equals='go_test'))
async def select_current_group(call: types.CallbackQuery):
    groups = await get_all_groups()
    keyboard = await groups_keyboard(groups=groups)
    await delete_test_row(call.from_user.id)
    await call.message.edit_text('Выберите необходимую для тестирования группу:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='group'))
async def get_admin_group(call: types.CallbackQuery):
    await delete_test_row(call.from_user.id)
    group = call.data.split('_')[1]
    await update_tests_group(group=group, telegram_id=call.from_user.id)

    lessons = await get_lessons()
    keyboard = await lesson_keyboard(lessons)
    await call.message.edit_text(f'Выберите дисциплину для группы {group}:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='lesson'))
async def get_admin_lesson(call: types.CallbackQuery):
    lesson = call.data.split('_')[1]
    await update_tests_lesson(lesson=lesson, telegram_id=call.from_user.id)

    categories = await get_categories(lesson)
    keyboard = await categories_keyboard(categories)

    await call.message.edit_text(f'Выберите необходимые категории вопросов для Дисциплины <b>{lesson}</b>',
                                 reply_markup=keyboard)


@dp.callback_query_handler(Text(endswith='true'))
async def change_state_category(call: types.CallbackQuery):
    category = call.data.split('_')[1]

    lesson = await update_category(telegram_id=call.from_user.id, category=category)
    keyboard = await edited_categories_keyboard(category_true=category, lesson=lesson)

    data = await get_categories_test(call.from_user.id)

    categories = data.split(" ")
    del categories[0]

    await call.message.edit_text(f'Выберите необходимые категории вопросов для Дисциплины <b>{lesson}</b>\n\n'
                                 f'Сейчас выбраны следующие категории: <b>{", ".join(categories)}</b>',
                                 reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='check'))
async def pre_check_test(call: types.CallbackQuery):
    data = await get_test_teacher_id(call.from_user.id)
    categories = data.categories.split(" ")
    del categories[0]
    await call.message.edit_text(f'Тестирование для группы {data.group}\n'
                                 f'Дисциплина: {data.lesson}\n\n'
                                 f'Категории вопросов: {", ".join(categories)}\n\n'
                                 f'<b>Выберите необходимое действие на клавиатуре:</b>', reply_markup=admin_final_menu)

@dp.callback_query_handler(Text(equals='start_test'))
async def start_testing(call: types.CallbackQuery):
    students = ''