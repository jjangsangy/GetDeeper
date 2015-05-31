from sodapy import Socrata

from multiprocessing.dummy import Pool as ThreadPool

import pandas as pd

API_KEY = 'iuM3ojETQCgrfPmd3HKD5C4JG'

def gen_data(filepath, api_key, username=None, password=None, output='csv'):
    api = Socrata('data.seattle.gov', api_key, username=username, password=password)

    with open(filepath) as fp:
        uid = [i.strip() for i in fp.readlines()]

    for dataset in uid:
        yield {dataset: api.get('/resource/' + dataset + '.' + output)}

def download():
    data = gen_data('viewids', API_KEY)
    for d in data:
        name, value = d.items()[0]
        print(name)
        df = pd.DataFrame.from_dict(value)
        df.to_csv(name + '.csv')

