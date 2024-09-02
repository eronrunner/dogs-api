import os.path
from os import listdir
from os.path import isfile, join

ROOT_DIR = os.path.abspath("../")


def ls_all_files_in_directory(directory: str) -> [str]:
    for f in listdir(directory):
        if isfile(join(directory, f)):
            yield directory, f


def path_to_file(file: str) -> str:
    return os.path.join(ROOT_DIR, *file.split("/"))
