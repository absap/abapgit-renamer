import os
import argparse
import re
from collections import OrderedDict

test_mode = False
start_dir = ''
rename_direction = 'ZS'


class CLIOption(object):
    pass


options = CLIOption()


def parse_cmd_args():
    global test_mode, start_dir, rename_direction

    parser = argparse.ArgumentParser(description='Renamer Options')
    parser.add_argument('--dir',
                        help='abapGit Directory',
                        nargs='?',
                        required=True)
    parser.add_argument('--direction',
                        help='renaming direction SAP->Z/Y or Z/Y->SAP',
                        choices=['SZ', 'ZS'])
    parser.add_argument('--test', '-t',
                        help='Test Mode',
                        action="store_true")

    parser.parse_args(namespace=options)

    if options.test:
        test_mode = True
        print('Test Mode On, NO CHANGE operations will be triggered!')

    if options.dir is not None:
        start_dir = options.dir
        print('Start Directory:', start_dir)

    if options.direction is not None:
        rename_direction = options.direction
        print('Directory:', rename_direction)


def add_z_namespace(expr):
    char = 'z' if expr.islower() else 'Z'
    return char


def rename(path, file):
    global test_mode, start_dir, rename_direction
    # print(file[1:])
    old_file_path = os.path.join(path, file)
    # print(old_file_path)
    if file != 'package.devc.xml':
        if rename_direction == 'ZS':
            new_file_path = os.path.join(path, file[1:])
        elif rename_direction == 'SZ':
            char = add_z_namespace(file)
            new_file_path = os.path.join(path, char + file)
    else:
        new_file_path = os.path.join(path, file)

    if not test_mode:
        os.rename(old_file_path, new_file_path)


def matcher(expr, content):
    regex = re.compile(expr)
    matcher = regex.finditer(content)
    matches = []
    if matcher:
        for match in matcher:
            matches.append(match.group())

    matches = list(OrderedDict.fromkeys(matches))
    return matches


def replace_content(file):
    global test_mode, start_dir, rename_direction

    _, ext = os.path.splitext(file)

    if ext in ['xml', 'abap']:
        with open(file, 'r') as f:
            content = f.read()
            # # https://docs.python.org/3/library/re.html#re.match.group

            expr = r""
            if rename_direction == 'ZS':
                expr = r"(zcl_|zif_|zcx_|ZCL_|ZIF_|ZCX_|ZABAPGIT|zabapgit|EZABAPGIT)"
            elif rename_direction == 'SZ':
                expr = r"(cl_abapgit|if_abapgit|cx_abapgit|cl_abapgit|if_abapgit|cx_abapgit|a4c_agit_adt|cx_adt_rest_abapgit)"

            matches = matcher(expr, content)

            for expr in matches:
                if rename_direction == 'ZS':
                    if 'EZABAPGIT' in expr:
                        content = content.replace(expr, 'EABAPGIT')
                    else:
                        content = content.replace(expr, expr[1:])
                elif rename_direction == 'SZ':
                    char = add_z_namespace(expr)
                    content = content.replace(expr, char + expr)

        if not test_mode:
            with open(file, 'w') as f:
                f.write(content)


def main():
    global test_mode, start_dir, rename_direction

    for root, dirs, files in os.walk(start_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            print(len(path) * '---', file)
            file_path = os.path.join(os.path.abspath(root), file)
            replace_content(file_path)

            rename(os.path.abspath(root), file)


if __name__ == "__main__":
    parse_cmd_args()
    main()
