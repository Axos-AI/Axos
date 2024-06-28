"""an agent that chats with the user. takes in repo details and answers user questions about the repo. should be extended to have refactor changes in its context.
"""
from langchain_openai import ChatOpenAI
from src.config.config import OPENAI_API_KEY, model_name
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.models.question_context import QuestionContext
from src.utils.utils import format_documents
from src.utils.file_processing import search_documents, get_github_repo_structure

class ChatAgent:
    def __init__(self, openai_api_key: str = OPENAI_API_KEY,  model_name: str = model_name, temperature: float = 0.3, conversation_history="", chat_template="", chat_prompt=None):
        # Instantiate the ChatOpenAI model with the desired parameters
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name, temperature=temperature)

        self.chat_template = chat_template if chat_template else """
            You are an experienced lead developer reviewing a GitHub repository. 

            Conversation so far: {conversation_history} | 
            
            You have been asked the following question: {question} | 

            Here are the details of the repository: {repo_name} ({github_url}) | 
            
            Relevant Files: {numbered_documents}  | 
            
            File Count: {file_type_counts} | 
            
            File Names: {file_names} | 
            
            File Structure: {file_structure} | 

            Answer:
            """        

        self.chat_prompt = chat_prompt if chat_prompt else PromptTemplate(
                template=self.chat_template,
                input_variables=["repo_name", "github_url", "conversation_history", "question", "numbered_documents", "file_type_counts", "file_names", "file_structure"]
            )
        self.chain = self.chat_prompt |  self.llm | StrOutputParser()

        self.conversation_history = conversation_history



    def ask_question_with_context(self, question, context: QuestionContext) -> str: # TODO update to take in different context/parameters
        print(f"Searching for relevant documents for question: '{question}'...")
        relevant_docs = search_documents(question, context.index, context.documents, n_results=5)
        print(f"Found {len(relevant_docs)} relevant documents.")

        numbered_documents = format_documents(relevant_docs)

        print("Invoking the language model to answer the question...")

        try:
            answer_with_sources = self.chain.invoke({
                "repo_name": context.repo_name,
                "github_url": context.github_url,
                "conversation_history": self.conversation_history,
                "question": question,
                "numbered_documents": numbered_documents,
                "file_type_counts": context.file_type_counts,
                "file_names": context.file_names,
                "file_structure": context.file_structure
            })
            self.conversation_history += f"Question: {question}\nAnswer: {answer_with_sources}\n"
        except Exception as e:
            print(f"Error invoking language model: {e}")
            answer_with_sources = "N/A"
        return answer_with_sources
