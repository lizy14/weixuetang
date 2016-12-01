import aiohttp
import asyncio
from .config import *

session = aiohttp.ClientSession(loop=loop)

async def wrapped_json(path, payload={}): # path starts with '/'
    auth = {
        'apikey': API_KEY,
        'apisecret': API_SECRET
    }
    body = {**auth, **payload} # merge two dicts
    r = await session.post(URL_PREFIX + path, data=body)
    return await r.json()
