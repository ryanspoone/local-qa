import os
from dotenv import load_dotenv
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle

# Load the environment variables from the .env file
load_dotenv()


# Function to read text files from a given directory
def read_files(file_path):
    return list(Path(file_path).glob("**/*.txt"))


# Get the absolute path of the main.py file
main_path = os.path.abspath("main.py")
# Get the parent directory of the main.py file
parent_directory = os.path.dirname(main_path)
# Define the relative path of the context files
file_path = os.path.join(parent_directory, "context")

# Read the text files in the context directory
ps = read_files(file_path)

# Load the data from the text files
data = []
sources = []
for p in ps:
    with open(p) as f:
        data.append(f.read())
    sources.append(p)

# Split long documents into smaller chunks due to the context limits of the LLMs
text_splitter = CharacterTextSplitter(chunk_size=1500, separator="\n")
docs = []
metadatas = []
for i, d in enumerate(data):
    splits = text_splitter.split_text(d)
    docs.extend(splits)
    metadatas.extend([{"source": sources[i]}] * len(splits))

# Create an OpenAI embeddings object with the API key
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

# Create a vector store from the documents and save it to disk
store = FAISS.from_texts(docs, embeddings, metadatas=metadatas)
faiss.write_index(store.index, "docs.index")
store.index = None
with open("faiss_store.pkl", "wb") as f:
    pickle.dump(store, f)
