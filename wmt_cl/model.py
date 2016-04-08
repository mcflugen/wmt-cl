#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import argparse
import json

import yaml
import requests


from .constants import PREFIX


def get(id, prefix=None):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'models/show/{id}'.format(id=id))

    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    try:
        return yaml.load(resp.text)
    except ValueError:
        raise RuntimeError('unable to convert response to JSON')


def list(prefix=None):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'models/list')

    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    try:
        return yaml.load(resp.text)
    except ValueError:
        raise RuntimeError('unable to convert response to JSON')


def save(model, prefix=None):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'models/new')

    payload = {
        'name': model['name'],
        'json': json.dumps(model),
    }

    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))

    try:
        return int(resp.text)
    except ValueError:
        raise RuntimeError(
            '{resp}: unexpected response '
            '(expecting int)'.format(resp=resp.text))


def upload_file(id, path_to_file, prefix=None):
    prefix = prefix or PREFIX
    url = os.path.join(prefix, 'models/upload')

    payload = {
        'id': id,
    }
    files = {
        'file': (os.path.basename(path_to_file), open(path_to_file, 'r')),
    }

    resp = requests.post(url, data=payload, files=files)
    if resp.status_code != 200:
        raise RuntimeError(
            '{code}: unexpected response code'.format(code=resp.status_code))
