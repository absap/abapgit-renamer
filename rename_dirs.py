import os
import argparse

start_dir = ''
test_mode = False


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


def rename_directoy(name):
    global test_mode
    abs_path = os.path.abspath(name)

    dir_name = os.path.dirname(abs_path)
    # print(dir_name)
    old_name = os.path.basename(name)

    if os.path.basename(dir_name) != 'src':
        # print(os.path.basename(dir_name))
        new_name = ''.join(
            ['a4c_clm_agit_', os.path.basename(dir_name), '_', old_name])
    else:
        new_name = ''.join(['a4c_clm_agit_', old_name])

    if not test_mode:
        os.rename(os.path.join(dir_name, old_name), os.path.join(dir_name, new_name))
    print("{0} -> {1}".format(old_name, new_name))


def main():
    global test_mode, start_dir
    for root, dirs, files in os.walk(start_dir, topdown=False):
        if not root == start_dir:
            rename_directoy(root)


if __name__ == "__main__":
    parse_cmd_args()
    main()
