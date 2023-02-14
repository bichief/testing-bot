from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp


@dp.callback_query_handler(Text(startswith='pass_test'))
async def exam_students(call: types.CallbackQuery, state=FSMContext):
    await state.reset_state(False)
    await call.message.edit_text('Успешно!')
