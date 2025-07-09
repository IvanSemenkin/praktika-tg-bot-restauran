from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.storage.utils.prompt import get_prompt
from src.storage.utils.logger import logger
from src.storage.utils.log_user_action import log_user_action
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from groq import Groq

loader = DirectoryLoader(
    "knowledge_base/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)


llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.4
)

parser = StrOutputParser()

documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(docs, embeddings)


def build_chain(prompt_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_text)
    ])
    return prompt | llm | parser

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
    rag_context = ""
    for doc in rag_results:
        rag_context += doc.page_content + "\n"

    prompt_text = get_prompt(history_context, rag_context, mess)


    chain = build_chain(prompt_text)
    response = chain.invoke({})


    logger.info(log_user_action(message, f'Ответ от ИИ: "{response}"'))
    return response