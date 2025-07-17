from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import AI
from src.bot.ai import ai_qwen_langchain
from src.utils.log_user_action import log_user_action
from src.utils.format_history_for_ai import format_history_for_ai
import asyncio

from src.utils import logger

admin_id = 1126700956
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    log_user_action(message, 'Старт')
    await message.answer(f"Привет, {message.from_user.first_name}", reply_markup=kb.main)


@router.message(F.text.lower() == "ии")
async def ai_start(message: Message, state: FSMContext):
    log_user_action(message, 'Запущен ИИ')
    await state.set_state(AI.wait_btn)
    await message.answer(
        'Выберете ваш тип запроса:', 
        reply_markup=kb.ai_keyboard)


@router.message(AI.wait_btn)
async def wait_btn(message: Message, state: FSMContext):
    if message.text.lower() == "мировые кухни":
        await state.update_data(wait_btn="мировые кухни")
        log_user_action(message, 'Выбрана мировая кухня')
        text = 'Что бы вы хотели спросить по мировым кухням?\n\nСпросите в формате `[русская] кухня`\n\nДля завершения напишите `Пока`, `Хватит`, `Стоп`'
    elif message.text.lower() == "выбор блюд":
        await state.update_data(wait_btn="выбор блюд")
        log_user_action(message, 'Выбран выбор блюд')
        text = 'Что бы вы хотели спросить по выбору блюд?\n\nСпросите в формате `хочу есть` или конкретнее `[прием пищи | погода | настроение | вкус]`\n\nДля завершения напишите `Пока`, `Хватит`, `Стоп`'
    else:
        await message.answer('Пожалуйста, выберите один из предложенных вариантов: "Сочитаемость блюд" или "Выбор блюд"' ,reply_markup=kb.ai_keyboard)
        return
    await state.set_state(AI.ask)
    await message.answer(text,  parse_mode="Markdown")
        
@router.message(AI.ask)
async def ai_ask(message: Message, state: FSMContext):
    if (
        message.text.lower() == "хватит"
        or message.text.lower() == "пока"
        or message.text.lower() == "стоп"
    ):
        await message.answer("Пока")
        log_user_action(message, 'Завершен ИИ')
        await state.clear()
        return

    log_user_action(message, f'Отправлено сообщение ИИ: "{message.text}"')
    
    data = await state.get_data()
    history = data.get("history", [])
    wait_btn = data.get("wait_btn")
    
    history_context = format_history_for_ai(history)
    ans = await asyncio.to_thread(
    ai_qwen_langchain, message.text, message, history_context, wait_btn
    )
    
    history.extend([
        {"role": "user", "content": message.text},
        {"role": "assistant", "content": ans}
    ])
    
    # if len(history) > 20:
    #     history = history[-20:]
    
    await state.update_data(history=history)
    
    
    try:
        await message.answer(ans, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Cannot parse .md {e} type: {type(e)}")
        clean_text = ans.replace("*", "").replace("_", "").replace("`", "")
        await message.answer(clean_text)




@router.message(F.text != '')
async def send_inf(message: Message):
    await message.answer('Для того чтобы включить нейросеть напишите "ИИ", для вывода информации напишите /info')
    log_user_action(message, 'Введена непонятная инфа')


