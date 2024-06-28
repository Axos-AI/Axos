class QuestionContext:
    def __init__(self, index, documents, repo_name, github_url, file_type_counts, file_names, file_structure):
        self.index = index
        self.documents = documents
        self.repo_name = repo_name
        self.github_url = github_url
        self.file_type_counts = file_type_counts
        self.file_names = file_names
        self.file_structure = file_structure