import os


def get_test_file_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), 'test_data/' + filename)
