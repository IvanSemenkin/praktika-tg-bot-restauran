from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.prompt import get_prompt, get_compatibility_prompt
from src.utils.logger import logger
from src.utils.log_user_action import log_user_action_formatter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.config import get_api_groq

loader = DirectoryLoader(
    "knowledge_base/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={'encoding': 'utf-8'}
)


llm = ChatGroq(
    model_name="gemma2-9b-it",
    temperature=0.4,
    api_key=get_api_groq(),
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

def ai_qwen_langchain(mess, message, history_context, wait_btn):

    rag_results = db.similarity_search(mess, k=3)
    rag_context = ""
    for doc in rag_results:
        rag_context += doc.page_content + "\n"
    
    if wait_btn == "сочетаемость блюд":
        prompt_text = get_compatibility_prompt(history_context, rag_context, mess)
    elif wait_btn == "выбор блюд":
        prompt_text = get_prompt(history_context, rag_context, mess)


    chain = build_chain(prompt_text)
    response = chain.invoke({})


    logger.info(log_user_action_formatter(message, f'Ответ от ИИ: "{response}"'))
    return response