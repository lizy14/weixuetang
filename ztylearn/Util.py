import aiohttp
import asyncio
from .config import *
import logging
import json
from datetime import *
import requests

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


def from_stamp(stamp):
    return date.fromtimestamp(stamp / 1000)


def wrap_date(dt):
    return int(dt.timestamp())


def parse_zty_stamp(st):
    return datetime.fromtimestamp(st / 1000)


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
    return EVENTS

    response = wrapped_json_sync('/events')
    assert(response['message'] == 'Success')
    events = response['events']

    def ignore_event(ev):
        name = ev['name']
        if name.startswith('研 '):
            return True
        if ('研究生' in name) and ('本科生' not in name):
            return True
        return False

    def wrap_event(ev):
        status = ev['status']
        status = {
            'begin': '开始',
            'end': '结束'
        }[status]
        today = datetime.combine(
            datetime.today().date(), datetime.min.time())

        return {
            'title': ev['name'].strip() + status,
            'date': wrap_date(today + timedelta(ev['remainingdays']))
        }

    return [wrap_event(ev) for ev in events if not ignore_event(ev)]


cached_week_info = None


def get_week_info():
    global cached_week_info
    if(cached_week_info):
        return cached_week_info

    response = wrapped_json_sync('/current')
    assert(response['message'] == 'Success')
    result = response['currentteachinginfo']

    cached_week_info = result
    return result
