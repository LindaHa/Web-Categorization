import pandas as pd


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
        domain = get_domain(page_url)
        if not not domain and domain not in domains:
            domains[domain] = domain
            pandas_row = [{'url': page_url, 'content': all_pages[page_url].content}]
            df = df.append(pandas_row)

    print('output')
    df['category'] = ''
    df.to_csv(output_path, index=False)


get_dark_web_data()


def get_domain_of_index(network: str, page_url: str) -> str:
    """
    :param network: the network of the url, such as .onion or .i2p
    :type network: str
    :param page_url: the url of the page
    :type page_url: str
    :return: the domain
    :rtype: str
    """
    if network in page_url and ' ' not in page_url:
        domain_parts = page_url.split(network)[:-1]
        domain = ''.join(domain_parts) + network

        return domain


def get_domain(page_url: str) -> str:
    """
    :param page_url: url of the page
    :type page_url: str
    :return: returns the domain of the page
    :rtype: str
    """
    domain = get_domain_of_index('.onion', page_url)
    if not domain:
        get_domain_of_index('.i2p', page_url)

    return domain
