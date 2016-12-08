import aiohttp
import asyncio
from .config import *
import logging
import json
from datetime import date
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
import requests

def from_stamp(stamp):
    return date.fromtimestamp(stamp / 1000)

async def wrapped_json(path, payload={}): # path starts with '/'
    _logger.debug("API %s param `%s`" % (path, payload))
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession(loop=loop)
    auth = {
        'apikey': API_KEY,
        'apisecret': API_SECRET
    }
    body = {**auth, **payload}  # merge two dicts
    r = await session.post(
        URL_PREFIX + path,
        data=json.dumps(body),
        headers={'content-type': 'application/json'}
    )
    resp_json = await r.json()
    session.close()
    return resp_json

def wrapped_json_sync(path, payload={}): # path starts with '/'
    _logger.debug("API SYNC %s param `%s`" % (path, payload))
    auth = {
        'apikey': API_KEY,
        'apisecret': API_SECRET
    }
    body = {**auth, **payload}  # merge two dicts
    r = requests.post(
        URL_PREFIX + path,
        data=json.dumps(body),
        headers={'content-type': 'application/json'}
    )
    resp_json = r.json()
    return resp_json

async def _register(username, password):
    result = await wrapped_json('/users/register', payload={
        'username': username,
        'password': password
    })
    assert(result['message'] == 'Success')

async def _unregister(username):
    result = await wrapped_json('/students/{username}/cancel'.format_map({
        'username': username
    }))
    assert(result['message'] == 'Success')

def register(username, password):
    result = wrapped_json_sync('/users/register', payload={
        'username': username,
        'password': password
    })
    assert(result['message'] == 'Success')

def unregister(username):
    result = wrapped_json_sync('/students/{username}/cancel'.format_map({
        'username': username
    }))
    assert(result['message'] == 'Success')
