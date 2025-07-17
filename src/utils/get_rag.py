from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def get_rag():
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    loader_food = DirectoryLoader(
        "knowledge_base_food/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    
    documents_food = loader_food.load()
    docs_food = text_splitter.split_documents(documents_food)
    
    db_food = FAISS.from_documents(docs_food, embeddings)
        
    ##########################################################################3
        
    loader_food_w = DirectoryLoader(
        "knowledge_base_world_cuisine/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    
    documents_food_w = loader_food_w.load()
    docs_food_w = text_splitter.split_documents(documents_food_w)
    
    db_food_w = FAISS.from_documents(docs_food_w, embeddings)
    return db_food_w, db_food
    
                    