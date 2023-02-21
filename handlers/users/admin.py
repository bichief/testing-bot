from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.exceptions import BotBlocked

from keyboards.inline.admin_final import admin_final_menu
from keyboards.inline.admin_menu import menu
from keyboards.inline.categories_keyboard import categories_keyboard, edited_categories_keyboard
from keyboards.inline.groups_keyboard import groups_keyboard
from keyboards.inline.lessons_keyboard import lesson_keyboard
from keyboards.inline.start_testing_students import go_test
from loader import dp
from states.start_student_test import StartTesting
from utils.db_api.db_commands import get_all_groups, update_tests_group, get_lessons, update_tests_lesson, \
    get_categories, update_category, get_categories_test, delete_test_row, get_test_teacher_id, get_students_group, \
    get_all_categories, add_questions_test


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

    keyboard = await categories_keyboard(lesson)

    await call.message.edit_text(f'Выберите необходимые категории вопросов для Дисциплины <b>{lesson}</b>',
                                 reply_markup=keyboard)


@dp.callback_query_handler(Text(endswith='true'))
async def change_state_category(call: types.CallbackQuery):
    category = call.data.split('_')[1]
    lesson = await update_category(telegram_id=call.from_user.id, category=category)
    keyboard = await edited_categories_keyboard(category_true=category, lesson=lesson)

    data = await get_categories_test(call.from_user.id)

    categories = data.split(" ")

    await call.message.edit_text(f'Выберите необходимые категории вопросов для Дисциплины <b>{lesson}</b>\n\n'
                                 f'Сейчас выбраны следующие категории: <b>{" ".join(categories)}</b>',
                                 reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='check'))
async def pre_check_test(call: types.CallbackQuery):
    data = await get_test_teacher_id(call.from_user.id)
    categories = data.categories.split(" ")
    del categories[0]
    await add_questions_test(categories, call.from_user.id)
    good_categories = await get_all_categories(categories)

    await call.message.edit_text(f'Тестирование для группы {data.group}\n'
                                 f'Дисциплина: {data.lesson}\n\n'
                                 f'Категории вопросов: {" ".join(good_categories)}\n\n'
                                 f'<b>Выберите необходимое действие на клавиатуре:</b>', reply_markup=admin_final_menu)


@dp.callback_query_handler(Text(equals='start_test'))
async def start_testing(call: types.CallbackQuery):
    data = await get_test_teacher_id(call.from_user.id)
    students = await get_students_group(data.group)
    keyboard = await go_test(test_id=data.id)

    await call.message.edit_text('Тестирование было успешно начато!\n'
                                 'Начинаю рассылку по студентам')
    for i in range(len(students)):
        state = dp.current_state(chat=students[i].telegram_id, user=students[i].telegram_id)
        await state.set_state(StartTesting.test.state)

        await state.update_data(
            {
                'array_questions': data.questions,
                'teacher_id': call.from_user.id
            }

        )

        try:
            await dp.bot.send_message(
                chat_id=students[i].telegram_id,
                text=f'👋 Началось новое тестирование для группы <b>{data.group}</b>!\n'
                     f'👨‍💻 Дисциплина - {data.lesson}\n\n'
                     f'✍ Нажми️ на кнопку ниже, чтобы приступить к решению вопросов\n'
                     f'🤞 Удачи!',
                reply_markup=keyboard
            )
        except BotBlocked:
            await call.message.answer(f'❌ Сообщение о начале тестирования не доставлено до {students[i].name}')
