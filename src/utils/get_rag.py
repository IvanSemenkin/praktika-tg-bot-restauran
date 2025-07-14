from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.utils.prompt import get_prompt, get_cuisine_info_prompt

def get_rag(wait_btn, mess, history_context):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if wait_btn == "выбор блюд":
        loader_food = DirectoryLoader(
            "knowledge_base_food/",
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        documents_food = loader_food.load()
        docs_food = text_splitter.split_documents(documents_food)
        
        db_food = FAISS.from_documents(docs_food, embeddings)
            
        rag_results = db_food.similarity_search(mess, k=3)
        rag_context = ""
        for doc in rag_results:
            rag_context += doc.page_content + "\n"
        prompt_text = get_prompt(history_context, rag_context, mess)
    elif wait_btn == "мировые кухни":
        loader_food = DirectoryLoader(
            "knowledge_base_world_cuisine/",
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        documents_food = loader_food.load()
        docs_food = text_splitter.split_documents(documents_food)
        
        db_food = FAISS.from_documents(docs_food, embeddings)
            
        rag_results = db_food.similarity_search(mess, k=3)
        rag_context = ""
        for doc in rag_results:
            rag_context += doc.page_content + "\n"
        prompt_text = get_cuisine_info_prompt(history_context, rag_context, mess)
        return prompt_text
    