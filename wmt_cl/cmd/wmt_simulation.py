from __future__ import print_function

import sys


def save(args):
    from ..model import get as model_get
    from ..simulation import save

    try:
        model = model_get(args.id)
    except RuntimeError:
        print('{id}: Unable to get model'.format(id=args.id))
        sys.exit(-1)
    else:
        name = args.name or model['name']

    try:
        sim_id = save(args.id, name, description=args.description)
    except RuntimeError as err:
        print('{err}: Unable to save simulation'.format(err=err),
              file=sys.stderr)
        sys.exit(1)
    else:
        print('{sim_id}'.format(sim_id=sim_id))


def launch(args):
    from ..simulation import launch

    stage(args)
    launch(args.id, username=args.username, password=args.password)


def stage(args):
    from ..simulation import stage

    stage(args.id)


def status(args):
    from ..simulation import status

    print('{status}'.format(status=status(args.id)))


def add_simulation_parser(parser):
    simulation_parser = parser.add_parser('simulation', help='WMT simulations')
    subparsers = simulation_parser.add_subparsers(
        title='subcommands', description='valid subcommands',
        help='additional help')

    parser_save = subparsers.add_parser('save', help='Save simulation')
    parser_save.add_argument('id', type=int, help='Model identifier')
    parser_save.add_argument('name', nargs='?', type=str, default=None,
                             help='Name for simulation')
    parser_save.add_argument('--description', default='None',
                             help='Description of the simulation')
    parser_save.set_defaults(func=save)

    parser_stage = subparsers.add_parser('stage', help='Stage simulation')
    parser_stage.add_argument('id', help='Simulation identifier')
    parser_stage.set_defaults(func=stage)

    parser_launch = subparsers.add_parser('launch', help='Launch simulation')
    parser_launch.add_argument('id', help='Simulation identifier')
    parser_launch.add_argument('--username', type=str, default=None,
                               help='Username for execution host')
    parser_launch.add_argument('--password', type=str, default=None,
                               help='Password for execution host')
    parser_launch.set_defaults(func=launch)

    parser_status = subparsers.add_parser('status',
                                          help='Get simulation status')
    parser_status.add_argument('id', help='Simulation identifier')
    parser_status.set_defaults(func=status)
