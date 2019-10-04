import pandas as pd

from typing import Dict, List

from Helpers.fetch_all_pages import ElasticSearchRepository


def domain_content() -> List[Dict[str, str]]:
    el_repository = ElasticSearchRepository()
    pages = el_repository.fetch_all()

    visited_domains = []
    urls_with_content = []
    for url, page in pages.items():
        domain = url.split('.onion')[0]
        if domain not in visited_domains:
            if page.content:
                url_content_pair = {'url': url, 'content': page.content}
                urls_with_content.append(url_content_pair)
                visited_domains.append(domain)

    return urls_with_content


date = '2019-03-10'
output_path = f'Datasets/Dark_web_dataset_{date}.csv'
pages_with_content = domain_content()

df = pd.DataFrame(pages_with_content, columns=["url", "content"])
df.to_csv(output_path, index=False)
