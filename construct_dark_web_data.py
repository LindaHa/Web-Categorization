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

nltk.download('stopwords')
nltk.download('words')
nltk.download('punkt')


def get_dark_web_data():
    char_blacklist = list(chr(i) for i in range(32, 127) if i <= 64 or i >= 91 and i <= 96 or i >= 123)
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(char_blacklist)
    language_whitelist = ['en']
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    blacklist_domain = ['.it', '.ru', '.cn', '.jp', '.tw', '.de', '.pl', '.fr', '.hu', '.bg', '.nl']

    dark_file_name = 'Datasets/Dark_web_dataset.csv'
    output_path = f'Datasets/Feature_dataset.csv'
    dark_df = pd.read_csv(dark_file_name)[['main_category', 'main_category:confidence', 'url', 'content']]
    dark_df = dark_df[(dark_df['main_category'] != 'Not_working') & (dark_df['main_category:confidence'] > 0.5)]
    dark_df['tokens_en'] = ''

    counter = 0
    for i, row in dark_df.iterrows():
        print(i)
        import pprint
        text = row['content']
        tokens = nltk.word_tokenize(text)
        allWordExceptStopDist = nltk.FreqDist(
            w.lower() for w in tokens if w not in stopwords and len(w) >= 3 and w[0] not in char_blacklist
        )

        all_words = [i for i in allWordExceptStopDist]
        pprint.pprint(row)

        if len(all_words) == 0:
            continue

        print(i)
        dark_df.at[i, 'tokens_en'] = all_words

    dark_df = dark_df[dark_df['tokens_en'] != '']
    dark_df.to_csv(output_path, index=False)


get_dark_web_data()