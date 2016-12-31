from userpage.models import *
from .models import get_appointments
from codex.apiview import APIView
from codex.baseerror import *
from wechat.wrapper import WeChatView
import json

from datetime import *

from ztylearn.Util import get_curriculum, get_events, get_week_info, parse_zty_stamp


def wrap_date(dt):
    return int(dt.timestamp())


def wrap_datetime(dt):
    return int(dt.timestamp())


def parse_date(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d')


class Personal(APIView):

    def get(self):
        try:
            start = parse_date(self.input['start'])
            end = parse_date(self.input['end'])
        except KeyError:
            start = None
            end = None

        return get_appointments(self.student.xt_id, start, end)


class Global(APIView):

    def get(self):
        return get_events()


class Semester(APIView):

    def get(self):
        week_info = get_week_info()

        开学日期 = parse_zty_stamp(
            week_info['currentsemester']['begintime']
        )
        学期名 = week_info['currentsemester']['name']
        校历第几周 = week_info['currentteachingweek']['name']

        return {
            'semester_name': 学期名,
            'semester_bagin': wrap_date(开学日期),
            'week_name': 校历第几周,
        }
