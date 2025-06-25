import requests
from src.storage.utils.logger import logger

def ai_qwen_langchain(mess, message, r):
    global chat_history

    history_context = ''
    for i in range(1, 11):
        try:
            history_context = history_context + f"user: {r.hget(f"chat_history:{message.from_user.id}:{i}", "user").decode()} \n\n" + f"assistant {r.hget(f"chat_history:{message.from_user.id}:{i}", "assistant").decode()} \n\n"
        except AttributeError:
            break
        

    prompt = (
        "Ты помощник в ресторане. "
        "Отвечай только на вопросы по теме еды, блюд, напитков, сервировки, кухни. "
        "Если вопрос не по теме — отвечай: 'Извините, я могу отвечать только по теме еды и ресторана.'"
        "Если есть хоть какой-то намек на еду, блюда, меню или что-то в этом роде - отвечай"
        "Отвечай на русском языке.\n\n"
        f"Вот история общения: {history_context}\n"
        f"А сейчас ответь **только** на: {mess}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3.1", "prompt": prompt, "stream": False},
    )

    response.raise_for_status()
    answer = response.json()["response"]

    return answer.strip()
