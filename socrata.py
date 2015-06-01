from __future__ import print_function

import os
import sys
import asyncio
import aiohttp
import time
import getpass
import json

from urllib.error import HTTPError
from pprint import pprint
from argparse import ArgumentParser

from sodapy import Socrata

@asyncio.coroutine
def fetch_page(url):
    headers = {'Conent-Type': 'Application/JSON'}
    session = aiohttp.ClientSession(connector=conn)
    response = yield from asyncio.wait_for(session.get(url), 0.001)
    yield from response.read()

@asyncio.coroutine
def gen_data(filepath, api_key, username=None, password=None, output='json'):
        api = Socrata('data.seattle.gov', api_key, username=username, password=password)

        with open(filepath) as fp:
            uid = set([i.strip() for i in fp.readlines()]) | set([i.strip() for i in open('completed.json')])

        for dataset in uid:
            print(dataset, file=open('completed.json', 'a'))
            yield {dataset: api.get('/resource/' + dataset + '.' + output)}

@asyncio.coroutine
def download(**auth):
    data = gen_data('viewids', **auth)
    stream = open('seattle.json')
    try:
        for d in data:
            if not isinstance(d, dict):
                continue
            print(d)
            print(', \n', file=stream)
            print(json.dumps(str(d), ensure_ascii=False, indent=4), file=stream)
    finally:
        return stream.close()

def check_viewids():
    return open('seattle.json', 'wt').close()

def command_line():
    parser = ArgumentParser()
    parser.add_argument('-l', nargs='*', metavar='login', const=None, dest='login', default=[])
    return parser.parse_args()

def auth():
    args, envar = command_line(), os.getenv('SOCRATA_API_KEY')
    api_key     = envar if envar else None
    username    = args.login if args.login else None
    password    = getpass.AskPassword('Password\n') if len(args.login) == 1 else None
    return {"api_key": api_key, 'username': username, 'password': password}

if __name__ == '__main__':
    check_viewids()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(download(**auth()))
    finally:
        loop.close()

