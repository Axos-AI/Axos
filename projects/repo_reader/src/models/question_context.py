from src.utils.file_processing import get_github_repo_structure


class QuestionContext:
    def __init__(self, vectorstore, repo_name, github_url, file_type_counts, file_names, file_structure=None):
        self.vectorstore = vectorstore
        self.repo_name = repo_name
        self.github_url = github_url
        self.file_type_counts = file_type_counts
        self.file_names = file_names
        self.file_structure = file_structure if file_structure else self.set_file_structure()

    def set_file_structure(self):
        try:
            self.file_structure = get_github_repo_structure( self.github_url)
        except Exception as e:
            print(f"Error getting repository structure: {e}")