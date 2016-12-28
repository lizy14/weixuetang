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


async def wrapped_json(path, payload={}):  # path starts with '/'
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


def wrapped_json_sync(path, payload={}):  # path starts with '/'
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


def get_curriculum(username):
    response = wrapped_json_sync('/curriculum/{username}'.format_map({
        'username': username
    }))
    assert(response['message'] == 'Success')
    return response['classes']


def get_events():
    return [
        {
            "name": "16-17春 研究生正选",
            "remainingdays": 1,
            "status": "begin"
        },
        {
            "name": "16-17春 二级选课",
            "remainingdays": 1,
            "status": "end"
        },
        {
            "name": "16-17春 研究生预选 ",
            "remainingdays": 1,
            "status": "end"
        },
        {
            "name": "研 个人培养计划维护 ",
            "remainingdays": 2,
            "status": "end"
        }
    ]
    response = wrapped_json_sync('/events')
    assert(response['message'] == 'Success')
    return response['events']


def get_week_info():
    return {
        "updatetime": 1482930943958,
        "currentsemester": {
            "name": "2016-2017-秋季学期",
            "id": "2016-2017-1",
            "begintime": 1473609600000,
            "endtime": 1487519999000
        },
        "currentteachingweek": {
            "name": "16",
            "id": "11065",
            "begintime": 1482681600000,
            "endtime": 1483286399000
        },
        "nextsemester": {
            "name": "2016-2017-春季学期",
            "id": "2016-2017-2",
            "begintime": 1487520000000,
            "endtime": 1498406399000
        }
    }
    response = wrapped_json_sync('/current')
    assert(response['message'] == 'Success')
    return response['currentteachinginfo']
