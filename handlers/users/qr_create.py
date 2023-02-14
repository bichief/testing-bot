import os

import qrcode
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InputFile
from aiogram.utils.deep_linking import get_start_link

from loader import dp
from states.get_group import GetGroup
from utils.db_api.db_commands import create_group


@dp.message_handler(Command('qr'))
async def get_group_name(message: types.Message):
    await message.answer('Введите кодировку группы\n\n'
                         'Например, ССА9521')

    await GetGroup.group.set()


@dp.message_handler(state=GetGroup.group)
async def creating_qr(message: types.Message, state: FSMContext):
    await state.reset_state(True)

    group = message.text

    data = await create_group(group)
    link = await get_start_link(data, encode=True)
    print(link)
    img = qrcode.make(link)
    img.save(f'QR Codes/{group}_qr.png')
    photo = InputFile(f'QR Codes/{group}_qr.png')

    await message.answer_photo(
        photo=photo,
        caption=f'QR код для группы {group} успешно создан!\n\n'
                f'Поделитесь фото со студентами или распечатайте его.'
    )
    os.remove(f'QR Codes/{group}_qr.png')
