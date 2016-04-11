#! /usr/bin/env python
from __future__ import print_function

import os

import yaml


def is_wmt_test_file(path):
    fname = os.path.basename(path)
    if fname.startswith('test_') and fname.endswith('.yaml'):
        with open(path, 'r') as fp:
            model = yaml.load(fp)
        if isinstance(model, dict):
            return 'model' in model and 'name' in model
    return False


def find_wmt_test_file(path):
    for item in os.listdir(path):
        if is_wmt_test_file(item):
            return os.path.join(path, item)
    return None


def find_wmt_test_data(path):
    data_files = []
    for item in os.listdir(path):
        if not is_wmt_test_file(item):
            data_files.append(os.path.join(path, item))
    return data_files


def run_test(args):
    from ..model import save, upload_file
    from ..simulation import save as save_sim
    from ..simulation import stage, launch

    test_file = find_wmt_test_file(args.path)
    print('test file: {fname}'.format(fname=test_file))

    if not test_file:
        return None

    with open(test_file, 'r') as fp:
        model_id = save(yaml.load(fp))
    print('model id: {model_id}'.format(model_id=model_id))

    for fname in find_wmt_test_data(args.path):
        upload_file(model_id, fname)

    sim_id = save_sim(model_id, os.path.basename(test_file),
                      description='wmt test')
    print('simulation id: {sim_id}'.format(sim_id=sim_id))

    stage(sim_id)
    launch(sim_id, username=args.username, password=args.password)


def find_tests(args):
    tests = []
    for dirpath, dirnames, filenames in os.walk(args.path):
        for fname in filenames:
            path_to_file = os.path.join(dirpath, fname)
            if is_wmt_test_file(path_to_file):
                tests.append(path_to_file)
    print('{tests}'.format(tests=os.linesep.join(tests)))


def add_test_parser(parser):
    test_parser = parser.add_parser('test', help='WMT tests')
    subparsers = test_parser.add_subparsers(title='subcommands',
                                            description='valid subcommands',
                                            help='additional help')

    test_run_parser = subparsers.add_parser('run', help='Run a model test')
    test_run_parser.add_argument('path', help='Path to test')
    test_run_parser.add_argument('--username', type=str, default=None,
                                 help='Username for execution host')
    test_run_parser.add_argument('--password', type=str, default=None,
                                 help='Password for execution host')
    test_run_parser.set_defaults(func=run_test)

    test_find_parser = subparsers.add_parser('find', help='Find tests')
    test_find_parser.add_argument('path', help='Base of directory to walk')
    test_find_parser.set_defaults(func=find_tests)
