# questions.py
from src.utils import format_documents
from src.file_processing import search_documents, get_github_repo_structure

class QuestionContext:
    def __init__(self, index, documents, llm_chain, repo_name, github_url, conversation_history, file_type_counts, filenames):
        self.index = index
        self.documents = documents
        self.llm_chain = llm_chain
        self.repo_name = repo_name
        self.github_url = github_url
        self.conversation_history = conversation_history
        self.file_type_counts = file_type_counts
        self.filenames = filenames

def ask_question(question, context: QuestionContext):
    print(f"Searching for relevant documents for question: '{question}'...")
    relevant_docs = search_documents(question, context.index, context.documents, n_results=5)
    print(f"Found {len(relevant_docs)} relevant documents.")

    numbered_documents = format_documents(relevant_docs)

    print("Invoking the language model to answer the question...")

    try:
        repo_structure = get_github_repo_structure(context.github_url)
    except Exception as e:
        print(f"Error getting repository structure: {e}")
        repo_structure = "N/A"

    try:
        answer_with_sources = context.llm_chain.invoke({
        "repo_name": context.repo_name,
        "github_url": context.github_url,
        "conversation_history": context.conversation_history,
        "question": question,
        "numbered_documents": numbered_documents,
        "file_type_counts": context.file_type_counts,
        "filenames": context.filenames,
        "file_structure": repo_structure
    })
    except Exception as e:
        print(f"Error invoking language model: {e}")
        answer_with_sources = "N/A"
    return answer_with_sources