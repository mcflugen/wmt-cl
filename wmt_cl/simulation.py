#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import argparse
import json
import getpass

import yaml
import requests


from .constants import PREFIX, HOST


def save(model_id, name, prefix=None, description='None'):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'run/new')

    payload = {
        'name': name,
        'model_id': model_id,
        'description': description,
    }

    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    return yaml.load(resp.text)


def stage(sim_id, prefix=None):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'run/stage')

    payload = {
        'uuid': sim_id,
    }

    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    return resp.text


def launch(sim_id, username=None, password=None, host=None, prefix=None):
    prefix = prefix or PREFIX
    host = host or HOST
    url = os.path.join(prefix, 'run/launch')
    username = username or getpass.getuser()
    password = password or getpass.getpass()

    payload = {
        'uuid': sim_id,
        'host': host,
        'username': username,
        'password': password,
    }

    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    return resp.text


def main():
    parser = argparse.ArgumentParser('Save a simulation.')
    parser.add_argument('id', type=int, help='Model identifier')
    parser.add_argument('name', nargs='?', type=str, default=None,
                        help='Name for simulation')
    parser.add_argument('--description', default='None',
                        help='Description of the simulation')

    args = parser.parse_args()

    try:
        model = get_model(args.id)
    except RuntimeError:
        print('{id}: Unable to get model'.format(id=args.id))
        sys.exit(-1)
    else:
        name = args.name or model['name']

    try:
        sim_id = save_simulation(args.id, name, description=args.description)
    except RuntimeError as err:
        print('{err}: Unable to save simulation'.format(err=err), file=sys.stderr)
        sys.exit(1)
    else:
        print('{sim_id}'.format(sim_id=sim_id))


if __name__ == '__main__':
    main()
