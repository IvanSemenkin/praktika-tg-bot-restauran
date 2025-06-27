import requests
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.storage.utils.prompt import get_prompt

loader = TextLoader("src/storage/utils/my-file.txt", encoding='utf-8')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
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
    rag_context = ""
    for doc in rag_results:
        rag_context += doc.page_content + "\n"

    prompt = get_prompt(history_context, rag_context, mess)

    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={"Content-Type": "application/json"},
        json={"model": "llama3.1", "prompt": prompt, "stream": False},
    )

    response.raise_for_status()
    return response.json()["response"].strip()
