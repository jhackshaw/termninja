import asyncio
import datetime
from functools import wraps
from sanic.response import json
from sanic.exceptions import abort


def throttle(max_per_minute=5, prefix=''):
    def decorator(f):
        @wraps(f)
        async def decorated(request, *args, **kwargs):
            now = datetime.datetime.now()
            key = f'{prefix}:{request.ip}:{now.minute}'
            res = await request.app.redis.get(key)
            if res and int(res) > max_per_minute:
                abort(429)
            trans = request.app.redis.multi_exec()
            trans.incr(key)
            trans.expire(key, 60)
            asyncio.create_task(trans.execute())
            return await f(request, *args, **kwargs)
        return decorated
    return decorator


def cache(key=None, seconds_until_expire=40, max_age=20):
    """

        seconds_until_expire: how long until response is recomputed
        max_age: how long the broser can hold on to it

        total potential cache time is seconds_until_expire + max_age

    """
    def decorator(f):
        @wraps(f)
        async def decorated(request, *args, **kwargs):
            cache_key = key or f.__name__
            cached = await request.app.redis.get(cache_key)
            if cached:
                res = json('')
                res.body = cached
                res.headers.update({
                    'Cache-Control': f'max-age={max_age}'
                })
            res = await f(request, *args, **kwargs)
            await request.app.redis.set(cache_key, res.body)
            return res
        return decorated
    return decorator
