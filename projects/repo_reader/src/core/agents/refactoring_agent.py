"""agent for refactoring code snippets using OpenAI's language model. Given a code snippet, the agent refactors the code using the language model. Should be extended to take multiple files and refactor them into modules.
"""
from langchain_openai import ChatOpenAI
from projects.repo_reader.src.utils.split_code import extract_chat_message, extract_code_block
from src.config.config import OPENAI_API_KEY, model_name

class RefactoringAgent:
    def __init__(self, openai_api_key: str = OPENAI_API_KEY,  model_name: str = model_name, temperature: float = 0.3):
        # Instantiate the ChatOpenAI model with the desired parameters
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name, temperature=temperature)

        # Define the system and user messages within the prompt template
        self.messages = [
            {"role": "system", "content": "You are an assistant that helps with code refactoring."}
        ]

    def refactor(self, code_snippet: str) -> str:
        """refactors within a code snippet

        Args:
            code_snippet (str): code snippet to refactor

        Returns:
            str: refactored code
        """

        # Define the user message within the prompt template
        self.messages.append({"role": "user", "content": f"Refactor the following code:\n\n{code_snippet}"})

        # Invoke the model with the defined prompt template
        response = self.llm.invoke(self.messages)

        # Extract and return the response content after stripping unnecessary characters
        model_response = response.content.strip()

        # Extract code block and chat message
        code_block = extract_code_block(model_response)
        chat_message = extract_chat_message(model_response)

        return code_block, chat_message