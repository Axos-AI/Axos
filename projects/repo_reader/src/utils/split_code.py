import re

def extract_code_block(model_response: str, language: str = "python") -> str:
    # Use regular expression to find code block for the specified language
    code_block_pattern = rf"```{language}(.*?)```"
    match = re.search(code_block_pattern, model_response, re.DOTALL)
    if match:
        code_block = match.group(1).strip()
    else:
        code_block = None
    return code_block

def extract_chat_message(model_response: str, language: str = "python") -> str:
    # Remove code block from the response
    code_block_pattern = rf"```{language}.*?```"
    message = re.sub(code_block_pattern, "", model_response, flags=re.DOTALL).strip()
    return message