import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

st.header("RHS Chatbot")

# Get input from user

# Extract the text
text = ""


with open("cleansed-data/all-data-cleansed.txt", 'r', encoding='utf-8') as file:
    for line in file:
        text += line

with open("cleansed-data/all-data-pdf-final.txt", 'r', encoding='utf-8') as file:
    for line in file:
        text += line

# Break it into chunks
text_splitter = RecursiveCharacterTextSplitter(
    separators="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)
chunks = text_splitter.split_text(text)
# st.write(chunks)

# generate embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
# create vector store - FAISS
vector_store = FAISS.from_texts(chunks, embeddings)

# - create embeddings with openai
# - initialize FAISS storage
# - store chunks and embeddigns

# get user question
user_question = st.text_input("Type your question here")

# do similarity search
if user_question:
    match = vector_store.similarity_search(user_question)
    # st.write(match)

    # define the LLM
    #streamlit run "C:\Users\aryav\IdeaProjects\Web Scraping ChatBot\chatbot.py"
    llm = ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        temperature = 0.4,
        max_tokens = 1000,
        model_name = "gpt-3.5-turbo"
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents = match, question = user_question)
    st.write(response)