from src.core.code_analyzer import CodeAnalyzer
from src.utils.file_processing import find_modified_files


if __name__ == "__main__":
    changed_files = find_modified_files()
    code_analyzer = CodeAnalyzer()
    adj_list = code_analyzer.get_adjacency_list()

    