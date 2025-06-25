# import os
# from langchain_openai import ChatOpenAI
# from langchain.schema import SystemMessage, HumanMessage
# from dotenv import load_dotenv
# from langchain.schema import SystemMessage, HumanMessage, AIMessage

# load_dotenv()


# llm = ChatOpenAI(
#     base_url=os.getenv("BASE_URL"),
#     api_key="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",
#     model=os.getenv("MODEL_NAME"),
#     temperature=0.7,
# )

# chat_history = []

# def ai_qwen_langchain(mess):
#     global chat_history
#     chat_history.append(HumanMessage(content=mess))
#     messages = [
#         SystemMessage(
#             content=(
#                 "Ты помощник в ресторане. "
#                 "Отвечай **только** на вопросы по теме еды, блюд, напитков, сервировки, кухни. "
#                 "Если вопрос не по теме — отвечай: 'Извините, я могу отвечать только по теме еды и ресторана.'"
#                 "Отвечай на русском языке"
#             )
#         ),
#         HumanMessage(content=mess),
#     ] + chat_history[-5:]

#     response = llm(messages)
#     chat_history.append(AIMessage(content=response.content))
#     return response.content


import requests

chat_history = []

def ai_qwen_langchain(mess: str) -> str:
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
        json={
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    answer = response.json()["response"]


    chat_history.append(f"Ассистент: {answer.strip()}")

    return answer.strip()



# from langchain_community.chat_models import ChatOllama

# from langchain.schema import SystemMessage, HumanMessage, AIMessage


# llm = ChatOllama(model="llama3.1")


# def ai_qwen_langchain(message: str) -> str:

#     system_message = SystemMessage(
#         content=(
#             "Ты помощник в ресторане. "
#             "Отвечай **только** на вопросы по теме еды, блюд, напитков, сервировки, кухни. "
#             "Если вопрос не по теме — отвечай: 'Извините, я могу отвечать только по теме еды и ресторана.' "
#             "Отвечай на русском языке."
#         )
#     )

#     messages = system_message + message

#     response = llm.invoke(messages)
#     return response.content
