import pandas as pd
import urllib.request
import nltk
import datetime
import os
from urllib.request import urlopen
from multiprocessing import Pool, cpu_count
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


def remove_stopwords(tokens):
    for i, token in enumerate(tokens):
        tokens[i] = ''.join([ch for ch in token if ch not in char_blacklist])
    tokens_sw = [w.lower() for w in tokens if w not in stopwords]
    tokens_lemmatize = [wnl.lemmatize(token) for token in tokens_sw]
    return tokens_lemmatize


def crawl(object):
    print(f"{object['i']}/{len(original_urls)} || {object['url']}")
    tokens_lemmatize = ''
    try:
        req = urllib.request.Request(object['url'], headers=hdr)
        html = urlopen(req, timeout=15).read()
        soup = BeautifulSoup(html, "html.parser")
        [tag.decompose() for tag in soup("script")]
        [tag.decompose() for tag in soup("style")]
        text = soup.get_text()
        tokens_lemmatize = tokenize(text)
    except Exception as inst:
        print(f"{object['i']}/{len(original_urls)} || {object['url']} FAILED. because of {inst}")
    return tokens_lemmatize


def tokenize(text):
    tokens_lemmatize = ''
    try:
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk.lower() for chunk in chunks if chunk)
        # Tokenize text
        tokens = [token.lower() for token in word_tokenize(text)]
        # Remove stopwords
        tokens_lemmatize = remove_stopwords(tokens)
    except Exception as inst:
        print(f"FAILED. because of {inst}")
    return tokens_lemmatize if len(tokens_lemmatize) else ''
    #     return page_tokens[object['i']]


def offline_crawl(object):
    tokens_lemmatize = ''
    try:
        text = object['content']
        tokens_lemmatize = tokenize(text)
    except Exception as inst:
        print(f"{object['i']} || {object['url']} FAILED. because of {inst}")
    return tokens_lemmatize


date = '2019-02-10'
original_path = f'Datasets/URL-categorization-DFE.csv'
dark_web_path = f'Datasets/dark_web_dataset.csv'
output_path = f'Datasets/Feature_dataset_{date}.csv'
if True or not os.path.isfile(output_path):
    original_data = pd.read_csv(original_path)[['url', 'main_category', 'main_category:confidence']]
    original_data['url'] = original_data['url'].map(lambda x: 'http://' + x)
    original_data = original_data[(original_data['main_category'] != 'Not_working') & (original_data['main_category:confidence'] >= 0.5)]
    dark_web_data = pd.read_csv(dark_web_path)[['url', 'main_category', 'main_category:confidence', 'content']]
    dark_web_data = dark_web_data[(dark_web_data['main_category'] != 'Not_working') & (dark_web_data['main_category:confidence'] >= 0.5)]

    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    wnl = WordNetLemmatizer()
    char_blacklist = list(
        chr(i) for i in range(32, 127) if (i <= 47 or i >= 58) and (i <= 64 or i >= 91) and (i <= 96 or i >= 123))
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(char_blacklist)

    start = datetime.datetime.now()
    print(start)
    original_urls = [{
        "i": index,
        "url": url
    } for index, url in enumerate(list(original_data['url'].values)) if index < 10]

    dark_urls = [{
        "i": index,
        "url": row['url'],
        "content": row['content']
    } for (index, row) in dark_web_data.iterrows()]

    original_data['tokens'] = ''
    dark_web_data['tokens'] = ''
    p = Pool(cpu_count() * 2)
    tokens = p.map(crawl, original_urls)
    dark_tokens = p.map(offline_crawl, dark_urls)
    original_data['tokens'][:len(tokens)] = tokens
    dark_web_data['tokens'][:len(dark_tokens)] = dark_tokens
    dark_web_data = dark_web_data.drop(columns="content")

    df = original_data.append(dark_web_data)
    stop = datetime.datetime.now()
    print(stop)
    exec_time = stop - start
    print(exec_time)
    df.to_csv(output_path, index=False)
