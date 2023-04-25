"""Python file to serve as the frontend"""
import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import pickle


# Load the environment variables from the .env file
load_dotenv()

# Load the LangChain.
index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index
chain = VectorDBQAWithSourcesChain.from_llm(
    llm=OpenAI(model_name="text-davinci-003", temperature=0.5), vectorstore=store
)


# From here down is all the StreamLit UI.
st.set_page_config(page_title="Local QA Bot", page_icon=":robot:")
st.header("Local QA Bot")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if user_input:
    result = chain({"question": user_input})
    output = f"Answer: {result['answer']}\nSources: {result['sources']}"

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
