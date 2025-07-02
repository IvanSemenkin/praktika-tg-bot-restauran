import os
import requests
from aiogram import Router
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.storage.utils.prompt import culinary_get_prompt, pairing_get_prompt
from src.storage.utils.logger import logger
from src.storage.utils.log_user_action import log_user_action
from langchain.agents import initialize_agent, Tool
from langchain_ollama.llms import OllamaLLM
import asyncio

loader = DirectoryLoader(
    "knowledge_base/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)
documents = loader.load()
router1 = Router()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)

def culinary(mess, context):
    logger.info('culinary_func')
    prompt = culinary_get_prompt(context, mess)
    return call_llm(prompt)

# def pairing(context, input):
#     logger.info('pairing_func')
#     prompt = pairing_get_prompt(context, input)
#     return call_llm(prompt)



def call_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3.1", "prompt": prompt, "stream": False},
    )
    logger.info(f'llm_response_end {response.json()['response']}')
    return response.json()["response"].strip()


def ai_multiagent_handler(mess, message, r):
    history_context = ''
    for i in range(1, 11):
        user = r.hget(f'chat_history:{message.from_user.id}:{i}', 'user')
        assistant = r.hget(f'chat_history:{message.from_user.id}:{i}', 'assistant')
        if not user or not assistant:
            break
        history_context += f"user: {user.decode()}\nassistant: {assistant.decode()}\n"


    rag_results = db.similarity_search(mess, k=3)
    
    rag_context = "Информация из базы знаний:\n"
    for doc in rag_results:
        filename = os.path.basename(doc.metadata['source'])
        rag_context += f"\n[Из файла {filename}]:\n{doc.page_content}\n"

    context = {
        "history": history_context,
        "rag": rag_context
    }
    
    tool = [
        Tool(name="CulinaryAssistant", func=lambda x: culinary(mess, context), description="Помощь с выбором еды"),
        # Tool(name="PairingAdvisor", func=lambda x: pairing(x, context), description="Сочетание блюд и напитков"),
    ]
    
    agent = initialize_agent(tools=tool, llm=OllamaLLM(model="llama3.1"), agent="zero-shot-react-description", verbose=False, max_iterations=1)
    logger.info('agent run')
    res = agent.invoke(mess)
    logger.info(f'Agent result: {res}')

    
    
    return res['output']