#!/usr/bin/env python3

"""
Script to generate a csv file containing urls for all dicom instances on the specified server.

The server should be passed as the arg
"""

import argparse
import json
import sys

import requests


def get_instances(server):
    '''
    Queries the server for all available instances, returned as a list.
    '''
    headers = {'Accept': 'application/dicom+json'}
    resp = requests.get(f'{server}/instances', headers=headers)
    return json.loads(resp.content)


def get_instance_attribute(instance_dict, attribute):
    attribute_map = {
        'instance_uid': '00080018',
        'study_uid': '0020000D',
        'series_uid': '0020000E'
    }

    code = attribute_map.get(attribute)
    if code is None:
        raise AttributeError('\n\n Unrecognised Attribute {}', attribute)

    try:
        return instance_dict.get(code).get('Value')[0]
    except AttributeError:
        raise AttributeError('\n\nInvalid DICOM type for this extraction!')


def get_instance_uid(instance_dict):
    '''
    Returns the InstanceUID of the queried (JSON) DICOM dictionary.
    Expected input: Instance
    '''
    try:
        return instance_dict.get('00080018').get('Value')[0]
    except AttributeError:
        raise AttributeError('\n\nInvalid DICOM type for this extraction!')


def get_instance_url(server, instance):
    '''
    Obtain the url for the instance represented by the given dict, on the given server
    '''
    instance_uid = get_instance_attribute(instance, 'instance_uid')
    study_uid = get_instance_attribute(instance, 'study_uid')
    series_uid = get_instance_attribute(instance, 'series_uid')

    return f'{server}/studies/{study_uid}/series/{series_uid}/instances/{instance_uid}'


def parse_args():
    '''
    Parse the commands
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('servername', help='Microsoft Medical Imaging Server base address')
    return parser.parse_args()


def main(argv):
    args = parse_args()

    # Obtain the instance descriptions
    instances = get_instances(args.servername)

    # Derive url for each instance found
    instance_urls = [get_instance_url(args.servername, instance) for instance in instances]

    # Write to a single-column csv file
    with open("dicom_instances.csv", 'w') as f:
        header = ['url']
        lines = header + instance_urls
        f.write('\n'.join(header + instance_urls) + '\n')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
