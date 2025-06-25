import requests

chat_history = []


def ai_qwen_langchain(mess):
    global chat_history

    chat_history.append(f"Пользователь: {mess}")

    history_context = "\n".join(chat_history[-10:])

    prompt = (
        "Ты помощник в ресторане. "
        "Отвечай только на вопросы по теме еды, блюд, напитков, сервировки, кухни. "
        "Если вопрос не по теме — отвечай: 'Извините, я могу отвечать только по теме еды и ресторана.'"
        "Если есть хоть какой-то намек на еду, блюда, меню или что-то в этом роде - отвечай"
        "Отвечай на русском языке.\n\n"
        f"{history_context}\n"
        f"Ассистент:"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3.1", "prompt": prompt, "stream": False},
    )

    response.raise_for_status()
    answer = response.json()["response"]

    chat_history.append(f"Ассистент: {answer.strip()}")

    return answer.strip()