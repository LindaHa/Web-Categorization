from Helpers.Models.link_model import Link
from typing import List


class Page(object):
    id: str
    url: str
    content: str
    title: str
    links: List[Link]

    def __init__(self, **kwargs):
        for field in ("id", "url", "content", "title", "links"):
            setattr(self, field, kwargs.get(field, None))