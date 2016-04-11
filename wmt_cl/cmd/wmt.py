#! /usr/bin/env python
import argparse

from .wmt_model import add_model_parser
from .wmt_simulation import add_simulation_parser
from .wmt_test import add_test_parser
from ..constants import PREFIX


def main():
    parser = argparse.ArgumentParser(
        description='Command line access to the the WMT')
    parser.add_argument('--prefix', default=PREFIX,
                        help="Prefix of the WMT API")

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    add_model_parser(subparsers)
    add_simulation_parser(subparsers)
    add_test_parser(subparsers)

    args = parser.parse_args()

    rtn = args.func(args)
    if rtn is not None and rtn != 0:
        parser.exit(status=1)


if __name__ == '__main__':
    main()
