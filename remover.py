import argparse
import os
import re

test_mode = False
start_dir = ''
include_list_name = ''


class CLIOption(object):
    pass


options = CLIOption()


def parse_cmd_args():
    global test_mode, start_dir, include_list_name

    parser = argparse.ArgumentParser(description='Renamer Options')
    parser.add_argument('--dir',
                        help='abapGit Directory',
                        nargs='?',
                        required=True)
    parser.add_argument('--test', '-t',
                        help='Test Mode',
                        action="store_true")
    parser.add_argument('--path', '-p',
                        help='Path to include list',
                        nargs='?',
                        required=True)

    parser.parse_args(namespace=options)

    if options.test:
        test_mode = True
        print('Test Mode On, NO CHANGE operations will be triggered!')

    if options.dir is not None:
        start_dir = options.dir
        print('Start Directory:', start_dir)

    if options.path is not None:
        include_list_name = options.path
        print('Include List Path:', include_list_name)


def read_include_list(file):
    with open(include_list_name, 'r') as f:
        include_list = [l.strip() for l in f]

    return include_list


def prepare_regex(include_list):
    string = ''
    for entry in include_list:
        string += '_object_{0}.clas|'.format(entry)

    return string[:-1]


def prep_remove(include_list, file_path):
    remove_list = []
    object_pattern = prepare_regex(include_list)
    object_pattern = '{0}{1}'.format(object_pattern, '|package.devc.xml|if_abapgit_|_comparison_|_oo_|_objects_')
    # print(object_pattern)
    pattern = re.compile(r"(" + object_pattern + ")")

    for file in file_path:
        match = pattern.search(file)

        if not match:
            remove_list.append(file)

    return remove_list


def remove(files):
    global test_mode

    for file in files:
        print('Removing file: {0}'.format(file))
        if not test_mode:
            os.remove(file)


def main():
    global test_mode, start_dir, include_list_name

    include_list = read_include_list(include_list_name)
    file_list = []
    for root, dirs, files in os.walk(start_dir):
        # path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            # print(len(path) * '---', file)
            file_path = os.path.join(os.path.abspath(root), file)
            file_list.append(file_path)

    remove_list = prep_remove(include_list, file_list)
    remove(remove_list)


if __name__ == "__main__":
    parse_cmd_args()
    main()
