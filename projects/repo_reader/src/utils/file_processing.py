# file_processing.py
import os
import uuid
import subprocess
from langchain_community.document_loaders import DirectoryLoader, NotebookLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import os

from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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

            split_documents.extend(split_docs)
        except Exception as e:
            print(f"Error splitting document {original_doc.metadata['source']}: {e}")

    chain = (
        {"doc": lambda x: x.page_content}
        | ChatPromptTemplate.from_template("Summarize the following document:\n\n{doc}")
        | ChatOpenAI(max_retries=0)
        | StrOutputParser()
    )
    summaries = chain.batch(split_documents, {"max_concurrency": 5})
    # Initialize a MultiVectorRetriever with Chroma as the vectorstore
    vectorstore = Chroma(embedding_function=OpenAIEmbeddings())
    byte_store = InMemoryByteStore()
    id_key = 'doc_id'  
    multi_vector_retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        byte_store=byte_store,
        id_key=id_key
    )

    doc_ids = [str(uuid.uuid4()) for _ in split_documents]

    summary_docs = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(summaries)
    ]
    print("Adding documents to the vectorstore...")
    multi_vector_retriever.vectorstore.add_documents(summary_docs)
    multi_vector_retriever.docstore.mset(list(zip(doc_ids, split_documents)))

    # We can also add the original chunks to the vectorstore if we so want
    for i, doc in enumerate(split_documents):
        doc.metadata[id_key] = doc_ids[i]
    multi_vector_retriever.vectorstore.add_documents(split_documents)

    return multi_vector_retriever, file_type_counts, [doc.metadata['source'] for doc in split_documents]

def search_documents(query, multi_vector_retriever, n_results=5):
    # Perform the search
    results = multi_vector_retriever.invoke(query, k=n_results)

    return results

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

            
def get_local_repo_structure(local_path):
    # Check if the local path exists
    if not os.path.exists(local_path):
        return f"Error: Path '{local_path}' does not exist."

    # Initialize a variable to hold the repository structure as a string
    repo_structure = f"Repository Structure for {local_path}:\n"

    # Call build_local_repo_structure to build the structure recursively
    repo_structure += build_local_repo_structure(local_path, "")

    return repo_structure

def build_local_repo_structure(local_path, indent):
    repo_structure = ""
    for item in os.listdir(local_path):
        item_path = os.path.join(local_path, item)
        if os.path.isfile(item_path):
            repo_structure += f"{indent}- {item}\n"
        elif os.path.isdir(item_path):
            repo_structure += f"{indent}+ {item}/\n"
            repo_structure += build_local_repo_structure(item_path, indent + "  ")
    return repo_structure
