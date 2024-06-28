import os


class CodeRefactorer:
    def __init__(self, repo_path, ai):
        self.repo_path = repo_path
        self.ai = ai

    def refactor(self):
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    with open(os.path.join(root, file), 'r') as f:
                        code = f.read()
                        refactored_code = self.ai.refactor(code)
                        with open(os.path.join(root, file), 'w') as f:
                            f.write(refactored_code)