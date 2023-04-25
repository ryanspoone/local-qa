# Local Files Question-Answering

🤖Ask questions to your local text files in natural language🤖

💪 Built with LangChain

🌲 Environment Setup

In order to set your environment up to run the code here, first install all requirements:

```bash
pip install -r requirements.txt
```

Then create a .env file in the root directory and set your OpenAI API key there (if you do not have one, get one [here](https://beta.openai.com/signup/)):

```bash
OPENAI_API_KEY=....
```

📄 What is in here?

- Example text files for context
- Python script to query local text files with a question
- Code to deploy on Streamlit
- Instructions for ingesting your own dataset

📊 Example Data

This repo uses example text files as context. You can replace them with your own text files to query your specific data.

💬 Ask a question

In order to ask a question, you need to run the Streamlit app:

```bash
streamlit run main.py
```

This will launch the Streamlit interface where you can ask questions and get answers based on the ingested text files.

🚀 Code to deploy on Streamlit

The code to run the Streamlit app is in `main.py`. Run it using the command mentioned above to start the chat interface.

🧑 Instructions for ingesting your own dataset

1. Place your text files in the `context` folder.
2. Run the following command to ingest the data:

```bash
python ingest.py
```

Now you're done! You can ask questions to your chatbot based on your own dataset:

```bash
streamlit run main.py
```


### File Tree

```
📦local-qa
 ┣ 📂context
 ┃ ┣ 📜file1.txt
 ┃ ┣ 📜file2.txt
 ┃ ┣ 📜file3.txt
 ┃ ┗ 📜file4.txt
 ┣ 📜.env.example
 ┣ 📜.gitignore
 ┣ 📜ingest.py
 ┣ 📜main.py
 ┗ 📜requirements.txt
 ```