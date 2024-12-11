import os

def getPath(fileName):
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    return os.path.join(current_dir, fileName)