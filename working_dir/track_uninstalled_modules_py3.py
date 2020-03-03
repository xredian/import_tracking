import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug',
                    help='displays lists of uninstalled modules',
                    action='store_true')
args = parser.parse_args()


def collect_imports(directory=os.getcwd()):
    """
    Allows to get all imports from scripts in the specified directory
    :param directory: full path
    :return: list of imports (no duplicates)
    """
    folder = [file for file in os.walk(directory)]
    imports = []
    for address, dirs, files in folder:
        for file in files:
            if file.endswith('.py'):
                with open(address + '/' + file, 'r', encoding='utf-8-sig') as f:
                    strings = f.read().splitlines()
                for string in strings:
                    if string.startswith('import '):
                        imports.append(string.replace('import ', ''))
                    elif string.startswith('from'):
                        imports.append(string.split(' ')[1])
    return list(set(imports))


def collect_uninstalled_modules(imports: list, not_installed=None):
    """
    Displays a list of uninstalled modules
    :param imports: list of all imports
    :param not_installed: list for uninstalled modules
    :return: list of uninstalled modules
    """
    if not_installed is None:
        not_installed = []
    for imp in imports:
        try:
            __import__(imp)
            # print(f'{str(imp)}: Module was installed')
        except ModuleNotFoundError:
            # print(f'{str(imp)}: There was no such module installed')
            not_installed.append(imp)
    return not_installed


def is_installed(imports: list):
    """
    Raises an ModuleNotFoundError if a module is not installed
    :param imports: list of all imports
    :return: OK if all imports is installed (or raises an error)
    """
    for imp in imports:
        try:
            __import__(imp)
        except ModuleNotFoundError:
            sys.tracebacklimit = 0
            raise ModuleNotFoundError()
    return print('OK')


if args.debug:
    print(collect_uninstalled_modules(collect_imports()))
else:
    print(is_installed(collect_imports()))
