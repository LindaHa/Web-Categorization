import datetime
import csv
import nltk
import numpy as np
import pandas as pd
import ast
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os.path

from typing import Dict, List

from Helpers.fetch_all_pages import ElasticSearchRepository


def get_dark_web_data():
    output_path = 'Datasets/Dark_web_dataset.csv'
    repository = ElasticSearchRepository()
    all_pages = repository.fetch_all()
    print('df')
    df = pd.DataFrame(columns=['url', 'category', 'content'])

    domains = {}
    print('for')
    for page_url in all_pages:
        if '.onion' in page_url and ' ' not in page_url:
            domain_parts = page_url.split('.onion')[:-1]
            domain = ''.join(domain_parts) + '.onion'
            if domain not in domains:
                domains[domain] = domain
                pandas_row = [{'url': page_url, 'content': all_pages[page_url].content}]
                df = df.append(pandas_row)

    print('output')
    df['category'] = ''
    df.to_csv(output_path, index=False)


get_dark_web_data()
