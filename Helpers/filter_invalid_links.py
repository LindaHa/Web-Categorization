from typing import Dict

from Helpers.Models.page_model import Page


def filter_non_scraped_links(pages: Dict[str, Page]) -> Dict[str, Page]:
    """
    :param pages: Original pages from the database with possible links to non-existent pages
    :type pages: Dict[Page]
    :return: Pages with links that point only to existing pages
    :rtype: Dict[Page]
    """
    for page_url in pages:
        page = pages[page_url]
        page.links = [link for link in page.links if link.link in pages]

    return pages
