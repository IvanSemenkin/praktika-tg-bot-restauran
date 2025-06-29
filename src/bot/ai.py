import os
import requests
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.storage.utils.prompt import get_prompt
from src.storage.utils.logger import logger
from src.storage.utils.log_user_action import log_user_action

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

def ai_qwen_langchain(mess, message, r):
    history_context = ''
    for i in range(1, 11):
        try:
            history_context += (
                f"user: {r.hget(f'chat_history:{message.from_user.id}:{i}', 'user').decode()} \n"
                f"assistant: {r.hget(f'chat_history:{message.from_user.id}:{i}', 'assistant').decode()} \n"
            )
        except AttributeError:
            break

    rag_results = db.similarity_search(mess, k=3)
    
    rag_context = "Информация из базы знаний:\n"
    for doc in rag_results:
        filename = os.path.basename(doc.metadata['source'])
        rag_context += f"\n[Из файла {filename}]:\n{doc.page_content}\n"

    prompt = get_prompt(history_context, rag_context, mess)

    logger.info(log_user_action(message, f'Сообщение "{mess}" отправлена ИИ'))
    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3.1", "prompt": prompt, "stream": False},
    )
    
    logger.info(log_user_action(message, f'Инфармация от ИИ отправлена {response.json()["response"].strip()}'))
    return response.json()["response"].strip()