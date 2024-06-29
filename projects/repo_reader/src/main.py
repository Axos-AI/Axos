#main.py
import tempfile
from src.core.code_analyzer import CodeAnalyzer
from src.core.code_refactorer import CodeRefactorer
from src.config.config import WHITE, GREEN, RESET_COLOR
from src.core.agents.chat_agent import ChatAgent
from src.core.agents.refactoring_agent import RefactoringAgent
from src.utils.file_processing import clone_github_repo, load_and_index_files
from src.models.question_context import QuestionContext
from src.utils.utils import format_user_question


def main(chat, refactor):
    
    github_url = input("Enter the GitHub URL of the repository: ")
    repo_name = github_url.split("/")[-1]
    print("Cloning the repository...")
    with tempfile.TemporaryDirectory() as local_path:
        if clone_github_repo(github_url, local_path):
            print("Repository cloned. Indexing files at: " + local_path)

            if not chat and not refactor:
                chat = True

            if refactor:        
                analyzer = CodeAnalyzer(local_path)
                analyzer.analyze()
                ai = RefactoringAgent()
                refactorer = CodeRefactorer(local_path, ai)
                refactorer.refactor()

            vectorstore, file_type_counts, file_names = load_and_index_files(local_path)
            print("Indexing complete.")
            
            if vectorstore is None:
                print("No documents were found to index. Exiting.")
                exit()

            if chat:
                chat_agent = ChatAgent()

                question_context = QuestionContext(vectorstore, repo_name, github_url, file_type_counts, file_names)
                while True:
                    try:
                        user_question = input("\n" + WHITE + "Ask a question about the repository (type 'exit()' to quit): " + RESET_COLOR)
                        if user_question.lower() == "exit()":
                            break
                        user_question = format_user_question(user_question)
                        print('Thinking...')
                        answer = chat_agent.ask_question_with_context(user_question, question_context)
                        print(GREEN + '\nANSWER\n' + answer + RESET_COLOR + '\n')
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        break


        else:
            print("Failed to clone the repository.")
