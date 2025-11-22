import os
from typing import List

def create_path(path_elements: List[str]):
    windows = os.name == 'nt'
    delimiter = '\\' if windows else '/'
    return delimiter.join(path_elements)
