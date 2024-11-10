"""
Script created to return all files from a given folder path, including files from subfolders.
"""
import os


def get_files_from_path(folder_path: str) -> list:
    """
    Returns a list with all files from given path, including files from subfolders
    :param folder_path: full path of folder
    :return: a list with all files under folder path
    """
    if not os.path.exists(folder_path):
        print(f'Given path does not exist: <{folder_path}>')
        return []
    files_list = []
    folder_content = os.listdir(folder_path)
    for file_name in folder_content:
        full_path = os.path.join(folder_path, file_name)
        if os.path.isfile(full_path):
            files_list.append(full_path)
        else:
            files_list.extend(get_files_from_path(full_path))
    return files_list


GIVEN_PATH = r'given path here'
files = get_files_from_path(GIVEN_PATH)

for file in files:
    print(file)

if type(files).__name__ == 'list':
    print("This is a list")

print(get_files_from_path.__doc__)
