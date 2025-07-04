import os
import requests
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.storage.utils.prompt import get_prompt
from src.storage.utils.logger import logger
from src.storage.utils.log_user_action import log_user_action
from langchain_ollama import OllamaLLM

loader = DirectoryLoader(
    "knowledge_base/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

def ai_qwen_langchain(mess, message, history):

    rag_results = db.similarity_search(mess, k=3)
    
    rag_context = "Информация из базы знаний:\n"
    for doc in rag_results:
        filename = os.path.basename(doc.metadata['source'])
        rag_context += f"\n[Из файла {filename}]:\n{doc.page_content}\n"

    prompt = get_prompt(history, rag_context, mess)

    logger.info(log_user_action(message, f'Сообщение "{mess}" отправлена ИИ'))
    llm = OllamaLLM(
        model="llama3.1",
        base_url="http://localhost:11434",
    )
    response = llm.invoke(prompt)
    
    logger.info(log_user_action(message, f'Инфармация от ИИ отправлена {response}'))
    return response