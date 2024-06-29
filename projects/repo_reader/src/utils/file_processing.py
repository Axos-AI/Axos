# file_processing.py
import os
import uuid
import subprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
from src.utils.utils import clean_and_tokenize
from langchain_community.document_loaders import DirectoryLoader, NotebookLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config.config import model_name
import requests
import os
import uuid

from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

def clone_github_repo(github_url, local_path):
    try:
        subprocess.run(['git', 'clone', github_url, local_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return False

def load_and_index_files(repo_path):
    extensions = ['txt', 'md', 'markdown', 'rst', 'py', 'js', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'scala', 'html', 'htm', 'xml', 'json', 'yaml', 'yml', 'ini', 'toml', 'cfg', 'conf', 'sh', 'bash', 'css', 'scss', 'sql', 'gitignore', 'dockerignore', 'editorconfig', 'ipynb']

    file_type_counts = {}
    documents_dict = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            ext = file.split('.')[-1]
            if ext in extensions:
                file_path = os.path.relpath(os.path.join(root, file), repo_path)
                try:
                    loader = None
                    if ext == 'ipynb':
                        loader = NotebookLoader(str(file_path), include_outputs=True, max_output_length=20, remove_newline=True)
                    else:
                        loader = DirectoryLoader(repo_path, glob=f'./{file_path}')

                    loaded_documents = loader.load() if callable(loader.load) else []
                    if loaded_documents:
                        if ext not in file_type_counts:
                            file_type_counts[ext] = 0
                        file_type_counts[ext] += len(loaded_documents)
                        for doc in loaded_documents:
                            file_id = str(uuid.uuid4())
                            doc.metadata['source'] = file_path
                            doc.metadata['file_id'] = file_id

                            # Create a summary for the document
                            # summarizer = ChatPromptTemplate.from_template("Summarize the following document:\n\n{doc}")
                            # summary = ChatOpenAI(temperature=0.2, model_name=model_name).generate_prompt(summarizer.format_prompt({"doc": doc.page_content}))
                            # doc.metadata['blurb'] = summary

                            documents_dict[file_id] = doc
                except Exception as e:
                    print(f"Error loading file '{file_path}': {e}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

    split_documents = []
    for file_id, original_doc in documents_dict.items():
        try:
            split_docs = text_splitter.split_documents([original_doc])
            for split_doc in split_docs:
                split_doc.metadata['file_id'] = original_doc.metadata['file_id']
                split_doc.metadata['source'] = original_doc.metadata['source']
                # split_doc.metadata['blurb'] = original_doc.metadata['blurb']

            split_documents.extend(split_docs)
        except Exception as e:
            print(f"Error splitting document {original_doc.metadata['source']}: {e}")
            
    # Initialize a MultiVectorRetriever with Chroma as the vectorstore
    vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
    byte_store = InMemoryByteStore()
    id_key = 'file_id'  
    multi_vector_retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=byte_store,
        id_key=id_key
    )
    # Store the documents and their summaries in the vectorstore
    multi_vector_retriever.vectorstore.add_documents(split_documents)

    return multi_vector_retriever, file_type_counts, [doc.metadata['source'] for doc in split_documents]

def search_documents(query, multi_vector_retriever, n_results=5):
    # Create the self-querying retriever
    attribute_info = [
        AttributeInfo(name="source", description="The source file path of the document"),
        AttributeInfo(name="file_id", description="The unique identifier of the document"),
        AttributeInfo(name="blurb", description="A short summary of the document")
    ]
    retriever = SelfQueryRetriever(
        vectorstore=multi_vector_retriever,
        attribute_info=attribute_info,
        llm=ChatOpenAI(temperature=0.2, model_name=model_name),
    )

    # Perform the search
    results = retriever.get_relevant_documents(query, k=n_results)

    return results

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def get_github_repo_structure(repo_url):
    # Extract username and repository name from the URL
    parts = repo_url.strip('/').split('/')
    username = parts[-2]
    repo_name = parts[-1]

    # Construct the API URL to fetch the repository contents
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents/"

    # Make a GET request to the GitHub API
    response = requests.get(api_url)
    if response.status_code == 200:
        repo_contents = response.json()

        # Initialize a variable to hold the repository structure as a string
        repo_structure = f"Repository Structure for {username}/{repo_name}:\n"
        repo_structure += build_repo_structure(repo_contents, "")
        return repo_structure
    else:
        return f"Failed to fetch repository contents. Status code: {response.status_code}"

def build_repo_structure(contents, indent):
    repo_structure = ""
    for item in contents:
        if item['type'] == 'file':
            repo_structure += f"{indent}- {item['name']}\n"
        elif item['type'] == 'dir':
            repo_structure += f"{indent}+ {item['name']}/\n"
            repo_structure += build_repo_structure(item['contents'], indent + "  ")
    return repo_structure