class Link(object):
    name: str
    link: str

    def __init__(self, **kwargs):
        for field in ("link", "name"):
            setattr(self, field, kwargs.get(field, None))
