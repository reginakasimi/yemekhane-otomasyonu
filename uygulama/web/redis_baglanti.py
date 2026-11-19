import os

import redis

_istemci = None


def redis_istemci():
    """Один общий клиент Redis на весь процесс."""
    global _istemci
    if _istemci is None:
        _istemci = redis.Redis(
            host=os.environ['REDIS_HOST'],
            port=int(os.environ.get('REDIS_PORT', '6379')),
            decode_responses=True,
        )
    return _istemci