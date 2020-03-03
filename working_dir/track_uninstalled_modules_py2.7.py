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
    folder = [file_ for file_ in os.walk(directory)]
    imports = []
    for address, dirs, files in folder:
        for file_ in files:
            if file_.endswith('.py'):
                with open(address + '/' + file_, 'r') as f:
                    strings = f.read().splitlines()
                for string in strings:
                    if string.startswith('import '):
                        imports.append(string.replace('import ', ''))
                    elif string.startswith('from'):
                        imports.append(string.split(' ')[1])
    return list(set(imports))


def enumeration(lst):
    imports = []
    for item in lst:
        if item.find(' as ') == -1:
            imports.append(item.split(', '))
        else:
            imports.append(item[:item.find(' as ')])
    flatten = []
    for lst in imports:
        if type(lst) == str:
            flatten.append(lst)
        else:
            flatten.extend(lst)
    return flatten


def collect_uninstalled_modules(imports, not_installed=None):
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
        except ImportError:
            # print(f'{str(imp)}: There was no such module installed')
            not_installed.append(imp)
    return not_installed


def is_installed(imports):
    """
    Raises an ModuleNotFoundError if a module is not installed
    :param imports: list of all imports
    :return: OK if all imports is installed (or raises an error)
    """
    for imp in imports:
        try:
            __import__(imp)
        except ImportError as err:
            sys.tracebacklimit = 0
            raise ImportError()
    return 'OK'


if args.debug:
    print(collect_uninstalled_modules(enumeration(collect_imports())))
else:
    print(is_installed(enumeration(collect_imports())))



