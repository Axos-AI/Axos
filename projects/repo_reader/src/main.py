#main.py
import os
import tempfile
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from src.config import WHITE, GREEN, RESET_COLOR, model_name
from src.utils import format_user_question
from src.file_processing import clone_github_repo, load_and_index_files
from src.questions import ask_question, QuestionContext

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    github_url = input("Enter the GitHub URL of the repository: ")
    repo_name = github_url.split("/")[-1]
    print("Cloning the repository...")
    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            index, documents, file_type_counts, filenames = load_and_index_files(local_path)
            if index is None:
                print("No documents were found to index. Exiting.")
                exit()

            print("Repository cloned. Indexing files...")
            llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.2, model_name=model_name)

            template = """
            You are a developer reviewing a GitHub repository. You have been asked the following question: {question}

            Here are the details of the repository:

            Repo: {repo_name} ({github_url}) | Conv: {conversation_history} | Relevant Files: {numbered_documents}  | FileCount: {file_type_counts} | FileNames: {filenames} | FileStructure: {file_structure}
            
            if the user asks a question about a specific file in the repository and it is in the Relevant Files, answer the question with the answer from the file. 

            Answer:
            """

            prompt = PromptTemplate(
                template=template,
                input_variables=["repo_name", "github_url", "conversation_history", "question", "numbered_documents", "file_type_counts", "filenames", "file_structure"]
            )

            chain = prompt | llm | StrOutputParser()

            conversation_history = ""
            question_context = QuestionContext(index, documents, chain, repo_name, github_url, conversation_history, file_type_counts, filenames)
            while True:
                try:
                    user_question = input("\n" + WHITE + "Ask a question about the repository (type 'exit()' to quit): " + RESET_COLOR)
                    if user_question.lower() == "exit()":
                        break
                    print('Thinking...')
                    user_question = format_user_question(user_question)

                    answer = ask_question(user_question, question_context)
                    print(GREEN + '\nANSWER\n' + answer + RESET_COLOR + '\n')
                    conversation_history += f"Question: {user_question}\nAnswer: {answer}\n"
                except Exception as e:
                    print(f"An error occurred: {e}")
                    break

        else:
            print("Failed to clone the repository.")
