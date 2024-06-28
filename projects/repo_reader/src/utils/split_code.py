import re

def extract_code_block(chat_response):
    # Use regular expression to find code block
    code_block_pattern = r"```(?:python|)(.*?)```"
    match = re.search(code_block_pattern, chat_response, re.DOTALL)
    if match:
        code_block = match.group(1).strip()
    else:
        code_block = None
    return code_block

def extract_chat_message(chat_response):
    # Remove code block from the response
    code_block_pattern = r"```(?:python|).*?```"
    message = re.sub(code_block_pattern, "", chat_response, flags=re.DOTALL).strip()
    return message