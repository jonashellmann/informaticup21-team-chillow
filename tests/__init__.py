import os


def read_test_file(filename: str) -> str:
    file = open(os.path.join(os.path.dirname(__file__), 'test_data/' + filename))
    content = file.read()
    file.close()
    return content
