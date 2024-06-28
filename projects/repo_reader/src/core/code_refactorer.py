import os


class CodeRefactorer:
    def __init__(self, repo_path, ai):
        self.repo_path = repo_path
        self.ai = ai

    def refactor(self):
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        code = f.read()
                        refactored_code, logged_changes = self.ai.refactor(code) # TODO first check if log is empty
                        
                    # Write the refactored code back to the original file
                    with open(file_path, 'w') as f:
                        f.write(refactored_code)
                    
                    # Create a log file next to the original file
                    log_file_path = file_path + '.log'
                    with open(log_file_path, 'w') as log_f:
                        log_f.write(logged_changes)