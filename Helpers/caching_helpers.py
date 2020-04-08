from typing import Any, Dict
import redis
import pickle
from Helpers.Models.page_model import Page


def redis_cache_complex_object(redis_key: str, complex_object: object) -> None:
    r = redis.Redis()
    pickled_obj = pickle.dumps(complex_object)
    r.set(redis_key, pickled_obj)


def redis_get_complex_object(redis_key: str) -> Any:
    r = redis.Redis()
    from_redis = r.get(redis_key)
    if from_redis:
        return pickle.loads(from_redis)
    return None


def get_cached_all_pages() -> Dict[str, Page]:
    return redis_get_complex_object('all_pages')


def cache_all_pages(pages: Dict[str, Page]) -> None:
    redis_cache_complex_object('all_pages', pages)


page_shelf_name = 'backup_db_response'
page_shelf_key_prefix = 'pages_batch_'
page_shelf_batch_count = 'backed_up'
pages_no_content = 'pages_without_content'
