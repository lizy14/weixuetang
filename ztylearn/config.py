import os
import json


from WeLearn.settings import CAMUS_API_SECRET, CAMUS_API_KEY, CAMUS_URL_PREFIX

API_SECRET = CAMUS_API_SECRET
API_KEY = CAMUS_API_KEY
URL_PREFIX = CAMUS_URL_PREFIX.rstrip('/')


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

EVENTS = json.load(open(os.path.join(__location__, 'calendar.json')))
