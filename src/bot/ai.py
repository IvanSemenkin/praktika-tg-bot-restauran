from src.utils.logger import logger
from src.utils.log_user_action import log_user_action_formatter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.get_rag import get_rag
from src.utils.prompt import get_prompt, get_cuisine_info_prompt
import os


os.environ["TOKENIZERS_PARALLELISM"] = "false"
db_food_w, db_food = get_rag()

llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.4,
)

parser = StrOutputParser()


def build_chain(prompt_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text)
    ])
    return prompt | llm | parser

def ai_qwen_langchain(mess, message, history_context, wait_btn):
    if wait_btn == "выбор блюд":
        rag_results = db_food.similarity_search(mess, k=3)
        rag_context = ""
        for doc in rag_results:
            rag_context += doc.page_content + "\n"
        prompt_text = get_prompt(history_context, rag_context, mess)
    elif wait_btn == "мировые кухни":
        rag_results = db_food_w.similarity_search(mess, k=10)
        rag_context = ""
        for doc in rag_results:
            rag_context += doc.page_content + "\n"
        prompt_text = get_cuisine_info_prompt(history_context, rag_context, mess)

    chain = build_chain(prompt_text)
    response = chain.invoke({})

    logger.info(log_user_action_formatter(message, f'Ответ от ИИ: "{response}"'))
    return response