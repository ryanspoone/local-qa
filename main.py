"""Python file to serve as the frontend"""
import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
import faiss
from langchain import OpenAI
from langchain.chains import VectorDBQAWithSourcesChain
import pickle
import openai

# Load the environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Load the FAISS index for local document search
index = faiss.read_index("docs.index")

# Load the document store for local document search
with open("faiss_store.pkl", "rb") as f:
    store = pickle.load(f)

store.index = index

# Create an instance of the VectorDBQAWithSourcesChain with the specified language model and vector store
chain = VectorDBQAWithSourcesChain.from_llm(
    # Initialize the OpenAI language model with the specified model name and temperature
    llm=OpenAI(model_name="text-davinci-003", temperature=0.5),
    # Provide the vector store, which contains the document embeddings and information
    vectorstore=store,
)


# Function to get an answer from the OpenAI API
def get_openai_answer(question: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{question}\n\nAnswer:",
        temperature=0.5,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].text.strip()


# Configure the Streamlit page
st.set_page_config(page_title="Local QA Bot", page_icon=":robot:")
st.header("Local QA Bot")

# Add a session state variable to track initialization status
if "initialized" not in st.session_state:
    st.session_state["initialized"] = False

# Set initialized to True once everything is loaded
st.session_state["initialized"] = True

# Initialize the past and generated session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


# Function to get the user input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Display a warning if the bot is not yet initialized
if not st.session_state["initialized"]:
    st.warning("Please wait, the bot is initializing...")
else:
    user_input = get_text()

    if user_input:
        # Get an answer from the local document store
        result = chain({"question": user_input})
        answer = result["answer"]
        sources = result["sources"]

        # If the local answer is unsatisfactory, get an answer from OpenAI API
        if answer.lower() in ["i don't know", "i do not know"]:
            answer = get_openai_answer(user_input)
            sources = "OpenAI API"

        output = f"Answer: {answer}\nSources: {sources}"

        # Append the user input and generated output to the session state
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

# Iterate through the stored generated answers and user questions
# in reverse order (starting from the most recent)
for i in range(len(st.session_state["generated"]) - 1, -1, -1):
    # Display the generated answer as a bot message
    # 'key' is used to create a unique identifier for each message
    message(st.session_state["generated"][i], key=str(i))

    # Display the corresponding user question as a user message
    # 'key' is also used here to create a unique identifier for each user message
    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
