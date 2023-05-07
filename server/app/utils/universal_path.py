import os


def universal_path(path: str) -> str:
    return os.path.join(*path.split("/"))
