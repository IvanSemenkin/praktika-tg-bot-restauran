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

loader_food = DirectoryLoader(
    "knowledge_base_food/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)

loader_world = DirectoryLoader(
    "knowledge_base_world_cuisine/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)


llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.4,
)

parser = StrOutputParser()

documents_food = loader_food.load()
documents_world = loader_world.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs_food = text_splitter.split_documents(documents_food)
docs_worl = text_splitter.split_documents(documents_world)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_food = FAISS.from_documents(docs_food, embeddings)
db_wolrd = FAISS.from_documents(docs_worl, embeddings)


def build_chain(prompt_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text)
    ])
    return prompt | llm | parser

def ai_qwen_langchain(mess, message, history_context, wait_btn):
    
    prompt_text = get_rag(wait_btn, mess, history_context)

    chain = build_chain(prompt_text)
    response = chain.invoke({})


    logger.info(log_user_action_formatter(message, f'Ответ от ИИ: "{response}"'))
    return response