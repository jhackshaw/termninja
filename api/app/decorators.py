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


def cache(key=None, seconds_until_expire=30, max_age=15):
    def decorator(f):
        @wraps(f)
        async def decorated(request, *args, **kwargs):
            cache_key = key or request.path
            cached = await request.app.redis.get(cache_key)
            if cached:
                res = json('')
                res.body = cached
            else:
                res = await f(request, *args, **kwargs)
                if res.status != 200:
                    print(res.status)
                trans = request.app.redis.multi_exec()
                trans.set(cache_key, res.body)
                trans.expire(cache_key, seconds_until_expire)
                asyncio.create_task(trans.execute())

            res.headers.update({
                'Cache-Control': f'max-age={max_age}'
            })
            return res
        return decorated
    return decorator
