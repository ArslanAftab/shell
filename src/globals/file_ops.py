'Module containing all file related methods used throughout the project'
import os
import re


def output_to_file(content: str, operation: str, file_name: str) -> None:
    'Write or append given content to given file'
    output_type = 'w+' if operation == '>' else 'a+'
    with open(file_name, output_type) as f:
        f.write(f'{"".join(content)}\n')


def search_file(content: str, file_name: str, multiple_locations: bool) -> list:
    'Search a file for the given content'
    matches = []
    # Remove apostrpohes from regular expression
    if content[0] == '\'' and content[-1] == '\'':
        content = content[1:-1]
    try:
        # Find content matches in the provided file
        with open(file_name, 'r') as f:
            for line in f.readlines():
                pattern = r''
                for c in content:
                    pattern += c
                for match in re.findall(pattern, line):
                    line = line.replace(match, match)
                    # If multiple location were given to the function that called this function
                    # the file name should also be outputted
                    if multiple_locations:
                        matches.append(f'{file_name}:{line}')
                    else:
                        matches.append(f'{line}')
    except UnicodeDecodeError:
        # Catch error when trying to read files not encoded with utf-8
        # These files will not be important so we can ignore the exception
        pass
    return matches


def get_file_line_list(file_name, reverse=False):
    'Get list of lines from a file'
    line_list = []
    with open(file_name) as file:
        line_list = list(file.readlines()) if not reverse else list(reversed(
            file.readlines()))
    # In case last line does not end in \n
    if line_list != []:
        if line_list[-1][-1] != '\n':
            line_list[-1] += '\n'
    return line_list


def search_directory(content: str, dir_name: str) -> list:
    'Recursively search all files in a directory for the given content'
    matches = []
    for f in get_all_files(dir_name):
        matches += search_file(content, f, multiple_locations=True)
    return matches


def get_all_files(dir_name: str) -> list:
    'Find all files in a subdirectory'
    files = []
    for (dir_path, _, file_names) in os.walk(dir_name):
        files += [os.path.join(dir_path, f) for f in file_names]
    return files
