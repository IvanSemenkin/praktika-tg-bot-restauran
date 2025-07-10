from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import AI, Clear_db, GetInfoID, DelInfoID, DelMyInfo
from src.storage.utils.logger import logger
from src.bot.ai import ai_qwen_langchain
from src.storage.utils.log_user_action import log_user_action
from src.storage.utils.format_history_for_ai import format_history_for_ai
from aiogram.fsm.context import FSMContext

admin_id = 1126700956
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    logger.info(log_user_action(message, 'Старт'))
    await message.answer(f"Привет, {message.from_user.first_name} , твой id: {message.from_user.id}", reply_markup=kb.main)


@router.message(F.text.lower() == "ии")
async def ai_start(message: Message, state: FSMContext):
    logger.info(log_user_action(message, 'Запущен ИИ'))
    await state.set_state(AI.ask)
    await message.answer(
        'Что бы вы хотели спросить? ИИ ответит только на вопросы по еде. Для завершения напишите "Пока", "Хватит", "Стоп"'
    )


@router.message(AI.ask)
async def ai_ask(message: Message, state: FSMContext):
    if (
        message.text.lower() == "хватит"
        or message.text.lower() == "пока"
        or message.text.lower() == "стоп"
    ):
        await message.answer("Пока")
        await state.clear()
        return

    logger.info(log_user_action(message, f'Отправлено сообщение ИИ: "{message.text}"'))
    
    data = await state.get_data()
    history = data.get("history", [])
    
    history_context = format_history_for_ai(history)
    ans = ai_qwen_langchain(message.text, message, history_context)
    
    history.extend([
        {"role": "user", "content": message.text},
        {"role": "assistant", "content": ans}
    ])
    
    # if len(history) > 20:
    #     history = history[-20:]
    
    await state.update_data(history=history)
    
    await message.answer(ans, parse_mode="Markdown") 




@router.message(F.text != '')
async def send_inf(message: Message):
    await message.answer('Для того чтобы включить нейросеть напишите "ИИ", для вывода информации напишите /info')
    logger.info(log_user_action(message, 'Введена непонятная инфа'))


