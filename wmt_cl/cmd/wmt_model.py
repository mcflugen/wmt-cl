#! /usr/bin/env python
from __future__ import print_function

import argparse

import yaml


def get(args):
    from ..model import get

    print(yaml.dump(get(args.id), default_flow_style=False))


def list(args):
    from ..model import list

    print(yaml.dump(list(), default_flow_style=False))


def save(args):
    from ..model import save

    model_id = save(yaml.load(args.file.read()))
    print('{model_id}'.format(model_id=model_id))


def upload_file(args):
    from ..model import upload_file

    upload_file(args.id, args.file)


def add_model_parser(parser):
    model_parser = parser.add_parser('model', help='WMT models')
    subparsers = model_parser.add_subparsers(title='subcommands',
                                             description='valid subcommands',
                                             help='additional help')

    model_list_parser = subparsers.add_parser('list', help='List models')
    model_list_parser.set_defaults(func=list)

    model_save_parser = subparsers.add_parser('save', help='Save model')
    model_save_parser.add_argument('file', type=argparse.FileType('r'),
                                   help='Model description YAML file.')
    model_save_parser.set_defaults(func=save)

    model_get_parser = subparsers.add_parser('get', help='Get model')
    model_get_parser.add_argument('id', type=int, help='Model identifier')
    model_get_parser.set_defaults(func=get)

    model_upload_parser = subparsers.add_parser('upload',
                                                help='Upload file for model')
    model_upload_parser.add_argument('id', type=int, help='Model identifier')
    model_upload_parser.add_argument('file', help='File to upload')
    model_upload_parser.set_defaults(func=upload_file)
