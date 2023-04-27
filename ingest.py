"""
ingest.py

This script ingests a set of text files, computes their embeddings using OpenAI's language model,
and stores the embeddings and associated metadata in a FAISS index and a vector store.

This process enables efficient similarity-based search and retrieval of relevant documents for
question-answering purposes in the local QA bot.

Usage:
1. Place your text files in the 'context' folder.
2. Run this script to preprocess the text files, compute embeddings, and create the FAISS index.
"""
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain.text_splitter import CharacterTextSplitter
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import pickle
import numpy as np
import json

# Load the environment variables from the .env file
load_dotenv()

# Load configuration from the JSON file
with open("config.json") as config_file:
    config = json.load(config_file)
supported_extensions = config["supported_extensions"]


# Function to read text files with supported extensions from a given directory
def read_files(file_path):
    file_list = []
    for ext in supported_extensions:
        file_list.extend(list(Path(file_path).glob(f"**/*{ext}")))
    return file_list


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
    with open(p, encoding="utf-8") as f:
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

# Compute embeddings for the documents
doc_embeddings = np.vstack([embeddings.embed_query(doc) for doc in docs])

# Create a vector store from the precomputed embeddings and save it to disk
store = FAISS.from_texts(docs, embeddings, metadatas=metadatas)
store.embeddings = doc_embeddings
faiss.write_index(store.index, "docs.index")
store.index = None
with open("faiss_store.pkl", "wb") as f:
    pickle.dump(store, f)
