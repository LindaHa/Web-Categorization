import requests
from typing import Dict, Union
from Helpers.Models.page_model import Page
from Helpers.caching_helpers import get_cached_all_pages, cache_all_pages
from Helpers.filter_invalid_links import filter_non_scraped_links
from Helpers.parsers import get_scroll_id, get_pages_from_json, get_hits

CHUNK_SIZE = 500


class ElasticSearchRepository(object):
    def __init__(self, **kwargs):
        self.server = "http://147.251.124.23:9200/"
        self.end_point_url = self.server + "tor,i2p/"

    def fetch_chunk(self, scroll_id, i) -> Union[str, None]:
        payload = {
            "scroll": "1m",
            "scroll_id": scroll_id
        }
        try:
            response = requests.post(self.server + "_search/scroll", json=payload)
            print(response.status_code)
            response.raise_for_status()
            print('text len')
            print(len(response.text))
            print('headers')
            print(response.headers)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def fetch_all(self) -> Dict[str, Page]:
        all_pages_cached = get_cached_all_pages()
        if all_pages_cached:
            return all_pages_cached

        payload = {
            "size": CHUNK_SIZE,
            "query": {
                "match_all": {}
            }
        }

        print('fetching')

        response = requests.post(self.end_point_url + "_search?scroll=1m", json=payload)
        final_pages = {}
        if response.status_code == 200:
            json = response.json()
            scroll_id = get_scroll_id(json)
            final_pages = get_pages_from_json(json)
            hits = get_hits(json)
            import pprint
            import sys
            i = 0

            while hits:
                chunk_json = self.fetch_chunk(scroll_id, i)
                scroll_id = get_scroll_id(chunk_json)
                hits = get_hits(chunk_json)
                pages = get_pages_from_json(chunk_json)

                if pages:
                    final_pages.update(pages)

                print(i)
                i += 1

        final_pages = filter_non_scraped_links(final_pages)

        cache_all_pages(final_pages)

        return final_pages
