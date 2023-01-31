from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from loader import dp
from states.get_name import GetName
from utils.db_api.db_commands import get_all_groups, create_student, update_student_name


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    deep_link = message.get_args()
    groups = await get_all_groups()
    if deep_link == '':
        await message.answer('☹️ <b>Бот доступен только студентам СКТ</b>')
    else:
        if deep_link in groups:

            await create_student(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                group=deep_link
            )
            await message.answer('✅Отлично!\n\n'
                                 '✍️<b> Теперь отправь мне свое Имя и Фамилию, как записано в журнале</b>\n\n'
                                 '(БЕЗ номера в журнале!)')

            await GetName.name.set()

        else:
            await message.answer('⛔️ Неккоректная кодировка группы.')


@dp.message_handler(state=GetName.name)
async def get_student_name(message: types.Message, state: FSMContext):
    name = message.text
    await update_student_name(
        telegram_id=message.from_user.id,
        name=name
    )

    await state.reset_state(True)

    await message.answer(f'👋 Приятно познакомиться, <b>{name.split(" ")[0]}</b>!\n'
                         f'🤖 Я - Бот СКТ, который поможет всем преподавателям и студентам в прохождении тестов!\n\n'
                         f'🤔 Что делать дальше?\n'
                         f'👉 Осталось дело за малым - ждать теста. Как только преподаватель отправит новый тест, я сразу сообщу тебе об этом!')
