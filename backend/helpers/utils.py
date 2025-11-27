import os

def create_path(path_elements: list[str]):
    windows = os.name == 'nt'
    delimiter = '\\' if windows else '/'
    return delimiter.join(path_elements)
