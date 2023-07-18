from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter 
from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import Chroma,FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from config import DefaultConfig
import pickle
from PyPDF2 import PdfReader
import os


CONFIG = DefaultConfig()

openai_api_key = os.environ.get('open_api_key')

def retrive_index():
    if os.path.exists("Acloud_ai.pkl"):
        with open("Acloud_ai.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:   
        # load document 
        loader = DirectoryLoader('./', glob="**/*.pdf") 
        documents = loader.load()
        # split the documents into chunks 
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200) 
        texts = text_splitter.split_documents(documents)
        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings(openai_api_key = openai_api_key) 
        # create the vectorestore to use as the index 
        VectorStore = FAISS.from_documents(texts, embedding=embeddings)
        with open(f"Acloud_ai.pkl", "wb") as f:
            pickle.dump(VectorStore, f) 
    # # expose this index in a retriever interface 
    retriever = VectorStore.as_retriever(search_type="similarity", search_kwargs={"k":2})
    return retriever

def get_chat_history(inputs) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"Human:{human}\nAI:{ai}")
    return "\n".join(res)

def define_llm():
    # Define the LLM
    llm = ChatOpenAI(
            temperature=0,
            openai_api_key=openai_api_key,
            model_name="gpt-3.5-turbo"
        )
    
    # GET INDEX
    retriever = retrive_index()
    # memory 
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True, output_key='answer') 
    # create a chain to answer questions
    print(1)
    conversation = ConversationalRetrievalChain.from_llm(llm=llm, retriever = retriever, chain_type="stuff",memory= memory,get_chat_history=get_chat_history)
    return conversation

def get_answers(user_query):
    try:
        conversation
    except NameError:
        conversation = define_llm()
        result = conversation({"question": user_query})
    else:
        result = conversation({"question": user_query})    
    return result.get('answer')
    
    
