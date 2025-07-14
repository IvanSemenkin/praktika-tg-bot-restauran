from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.prompt import get_prompt, get_cuisine_info_prompt
from src.utils.logger import logger
from src.utils.log_user_action import log_user_action_formatter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import get_groq_key
from src.utils.get_rag import get_rag


llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.4,
)

parser = StrOutputParser()
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_chain(prompt_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text)
    ])
    return prompt | llm | parser

def ai_qwen_langchain(mess, message, history_context, wait_btn):
    
    prompt_text = get_rag(wait_btn, mess, history_context, embeddings)

    chain = build_chain(prompt_text)
    response = chain.invoke({})


    logger.info(log_user_action_formatter(message, f'Ответ от ИИ: "{response}"'))
    return response