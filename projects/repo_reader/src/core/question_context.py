from src.core.file_processing import get_local_repo_structure


class QuestionContext:
    def __init__(self, index, documents, repo_name, local_path, file_type_counts, file_names, file_structure=None):
        self.index = index
        self.documents = documents
        self.repo_name = repo_name
        self.local_path = local_path
        self.file_type_counts = file_type_counts
        self.file_names = file_names
        self.file_structure = file_structure if file_structure else self.set_file_structure()

    def set_file_structure(self):
        try:
            self.file_structure = get_local_repo_structure(self.local_path)
        except Exception as e:
            print(f"Error getting repository structure: {e}")