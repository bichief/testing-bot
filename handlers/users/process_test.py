from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.exam_keyboard import exam_kb
from keyboards.inline.process_testing_kb import testing_kb
from loader import dp
from states.start_student_test import StartTesting
from utils.db_api.db_commands import get_question_id, update_correct_answers, get_correct_answers, drop_correct_answers


@dp.callback_query_handler(Text(startswith='pass_test'), state=StartTesting.test.state)
async def exam_students(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    all_questions = {}
    array_questions = data.get('array_questions')
    teacher_id = data.get('teacher_id')
    await state.reset_data()

    questions = array_questions.split(' ')
    del questions[-1]

    for i in range(len(questions)):
        all_questions['q_' + str(i)] = questions[i]
    all_questions['teacher_id'] = teacher_id

    await state.update_data(all_questions)
    keyboard = await testing_kb(list_id=0)
    await call.message.edit_text('Вопросы успешно загружены.\n\n'
                                 'Нажмите на кнопку ниже, чтобы приступить к решению вопросов', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='pre_start_'), state=StartTesting.test.state)
async def testing_process(call: types.CallbackQuery, state: FSMContext):
    correct_answer = call.data.split('_')[3]

    list_id = int(call.data.split('_')[2])
    data = await state.get_data()
    pk = data.get('q_' + str(list_id))
    if correct_answer.isdigit():
        past_pk = data.get('q_' + str(list_id - 1))
        old_question = await get_question_id(pk=past_pk)
        if int(old_question.correct_answer) == int(correct_answer):
            await update_correct_answers(student_id=call.from_user.id, value=1)
    else:
        pass

    needed_question = await get_question_id(pk=pk)
    keyboard = await exam_kb(list_id)
    try:
        await call.message.edit_text(f'<b>Вопрос №{list_id + 1}</b>\n\n'
                                     f'{needed_question.question}\n\n'
                                     f'Варианты ответа:\n'
                                     f'{needed_question.pool_answers}\n\n'
                                     f'Выберите необходимый вариант ответа', reply_markup=keyboard)
    except AttributeError:
        student = await get_correct_answers(call.from_user.id)
        await call.message.edit_text('Тестирование успешно завершено!\n'
                                     f'Ваш результат: {student.amount_correct_answers}\n\n'
                                     f'Спасибо!')
        teacher_id = data.get('teacher_id')
        await dp.bot.send_message(
            chat_id=teacher_id,
            text=f'Студент {student.name} закончил тестирование.\n'
                 f'Его результат: {student.amount_correct_answers}\n\n'
                 f'Один правильный ответ - один балл.'
        )
        await drop_correct_answers(call.from_user.id)
        await state.reset_state(True)
