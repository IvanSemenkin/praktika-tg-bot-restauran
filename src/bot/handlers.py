from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import src.bot.keyboards as kb
from aiogram.fsm.context import FSMContext
from src.bot.states import AI, Clear_db, GetInfoID, DelInfoID, DelMyInfo
from src.storage.utils.logger import logger
import redis
import os
from src.bot.ai import ai_qwen_langchain
from src.storage.utils.log_user_action import log_user_action

admin_id = 1126700956
router = Router()
r = redis.Redis(host="localhost", port="6380", db=0)


@router.message(CommandStart())
async def start(message: Message):
    logger.info(log_user_action(message, 'Старт'))
    await message.answer(f"Привет, {message.from_user.first_name} , твой id: {message.from_user.id}", reply_markup=kb.main)


@router.message(Command("info"))
async def help(message: Message):
    logger.info(log_user_action(message, 'Выведена инфармация'))
    user = ''
    ai = ''
    found = False

    for i in range(1, 11):
        try:
            key = f"chat_history:{message.from_user.id}:{i}"
            if not r.exists(key):
                break  
            user = user + f"{i}. {r.hget(key, 'user').decode()} \n\n"
            ai = ai + f"{i}. {r.hget(key, 'assistant').decode()} \n\n"
        except AttributeError:
            break
    if user or ai:
        found = True
    
    if not found:
        await message.answer("Ваша история общения пуста.")
    else:
        await message.answer(f"User: \n{user}")
        await message.answer(f"AI: \n{ai}")


@router.message(Command("cls"))
async def help(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await state.set_state(Clear_db.wait_clear)
        await message.answer('Вы уверены? (Да/Нет)')
    else:
        await message.answer('У вас не достаточно прав')
    

@router.message(Clear_db.wait_clear)
async def clear_w(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        r.flushdb()
        await state.clear()
        await message.answer('БД успешно очишена')
    elif message.text.lower() == 'нет':
        await message.answer('Очистка отменена')
        await state.clear()


@router.message(Command('get_all_key'))
async def ai_start(message: Message):
    if message.from_user.id == admin_id:
        all_keys = r.keys('*')
        if not all_keys:
            await message.answer("В базе данных нет ни одного ключа.")
            return
        ans = ''
        for key in all_keys:
            decoded = key.decode()
            ans += f"{decoded} \n"
        await message.answer(ans)
    else:
        await message.answer('У вас не достаточно прав')



@router.message(Command('get_info_id'))
async def get_info_id(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await state.set_state(GetInfoID.id)
        await message.answer("Введите ID по которому хотете получить информацию: ")
    else:
        await message.answer('У вас не достаточно прав')

@router.message(GetInfoID.id)
async def get_info_id(message: Message, state: FSMContext):
    exists = False
    for i in range(1, 11):
        if r.exists(f"chat_history:{message.text}:{i}"):
            exists = True
            break
        
    if not exists:
        await message.answer(f"Нет данных по ID: {message.text}. Проверьте правильность ввода.")
        await state.clear()
        return
    await state.set_data({'id': message.text})
    await state.set_state(GetInfoID.type_info)
    await message.answer("Выберите формат дынных: ", reply_markup=kb.type_mess)

@router.message(GetInfoID.type_info)
async def get_info_id(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    user_id = data.get('id')
    history_random_type = ''
    if message.text.lower() == 'перемешанный':
        for i in range(1, 11):
            try:
                history_random_type += (
                    f"user: {r.hget(f'chat_history:{user_id}:{i}', 'user').decode()} \n"
                    f"assistant: {r.hget(f'chat_history:{user_id}:{i}', 'assistant').decode()} \n"
                )
            except AttributeError:
                break
        await message.answer(f"История общения {user_id}")
        await message.answer(history_random_type)
    elif message.text.lower() == 'линейный':
        user = ''
        ai = ''
        for i in range(1, 11):
            try:
                user = user + f"{i}. {r.hget(f"chat_history:{user_id}:{i}", "user").decode()} \n\n"
                ai = ai + f"{i}. {r.hget(f"chat_history:{user_id}:{i}", "assistant").decode()} \n\n"
            except AttributeError:
                break
            
        await message.answer(f"История общения {user_id}:")
        await message.answer(f"{user}")
        await message.answer(f"{ai}")




@router.message(Command('del_info_id'))
async def get_info_id(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await state.set_state(DelInfoID.id)
        await message.answer("Введите ID по которому хотете удалить все ключи ")
    else:
        await message.answer('У вас не достаточно прав')
        

@router.message(DelInfoID.id)
async def del_info_id(message: Message, state: FSMContext):
    exists = False
    for i in range(1, 11):
        if r.exists(f"chat_history:{message.text}:{i}"):
            exists = True
            break
        
    if not exists:
        await message.answer(f"Нет данных по ID: {message.text}. Проверьте правильность ввода.")
        await state.clear()
        return
    
    await state.set_data({'id': message.text})
    await state.set_state(DelInfoID.wait_del)
    await message.answer(f"Вы уверены, что хотите удалить историю по ID {message.text}? (Да/Нет) ")



@router.message(DelInfoID.wait_del)
async def get_info_id(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    user_id = data.get('id')
    if message.text.lower() == 'да':
        for i in range(1, 20): 
            deleted_key = f"chat_history:{user_id}:{i}"
            if r.exists(deleted_key):
                r.delete(deleted_key)
        r.delete(f'{user_id}_counter')
        await message.answer(f'Были удалены ключи с ID: {user_id}')
    
    elif message.text.lower() == 'нет':
        await message.answer(f'Очистка по ID: {user_id} отменена')
        await state.clear()
    else:
        await state.clear()
        await message.answer('Не смог распознать, отмена')


@router.message(Command("del_my_info"))
async def help(message: Message, state: FSMContext):
    await state.set_state(DelMyInfo.wait_del)
    await message.answer('Вы уверены? (Да/Нет)')
    

@router.message(DelMyInfo.wait_del)
async def clear_w(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        for i in range(1, 20): 
            deleted_key = f"chat_history:{message.from_user.id}:{i}"
            r.delete(deleted_key)
        await state.clear()
        await message.answer('Ваша история была очищена')
    elif message.text.lower() == 'нет':
        await message.answer('Очистка отменена')
        await state.clear()



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

    ans = ai_qwen_langchain(message.text, message, r)
    
    
    us_count = r.incr(f"{message.from_user.id}_counter")
    
    
    if int(us_count) >= 10:
        r.set(f"{message.from_user.id}_counter", 0)
        logger.info('counter_clear')
    
    r.hset(f"chat_history:{message.from_user.id}:{us_count}", mapping={"user":message.text, "assistant":ans})
    
    await message.answer(ans, parse_mode="Markdown") 




@router.message(F.text != '')
async def send_inf(message: Message):
    await message.answer('Для того чтобы включить нейросеть напишите "ИИ", для вывода информации напишите /info')
    logger.info(log_user_action(message, 'Введена непонятная инфа'))


