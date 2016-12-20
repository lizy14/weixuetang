from userpage.models import *
from .models import *
from codex.apiview import APIView
from codex.baseerror import *
from wechat.wrapper import WeChatView

from datetime import *

from ztylearn.Util import get_curriculum, get_events, get_week_info


def wrap_date(dt):
    return dt.strftime('%Y-%m-%d')
    return int(dt.timestamp())


def wrap_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M')
    return int(dt.timestamp())


class Personal(APIView):

    def get(self):

        def flatten(list_of_lists):
            # 折叠一层
            # [[1,2], [3,[4,5]]] -> [1, 2, 3, [4, 5]]
            return [val for sublist in list_of_lists for val in sublist]

        def 处理一门课程(课程):
            该课程的事件们 = []
            课程名 = 课程['coursename']
            地点 = 课程['classroom']
            星期几 = 课程['time'][0]
            第几节 = 课程['time'][1]
            周次表 = 课程['week']
            for 周次减一 in range(16):
                if(not 周次表[周次减一]):
                    continue
                该周周一 = 第一周第一天 + timedelta(days=7 * 周次减一)
                日期 = 该周周一 + timedelta(days=星期几 - 1)
                起止时分 = 大节起止时分[第几节]
                开始 = 日期 + timedelta(hours=起止时分[0], minutes=起止时分[1])
                结束 = 日期 + timedelta(hours=起止时分[2], minutes=起止时分[3])
                该课程的事件们.append({
                    'title': 课程名,
                    'location': 地点,
                    'begin': wrap_datetime(开始),
                    'end': wrap_datetime(结束)
                })
            return 该课程的事件们

        纯纯课程列表 = get_curriculum(self.student.xt_id)
        大节起止时分 = {
            1: [8, 0, 9, 35],
            2: [9, 50, 12, 15],
            3: [13, 30, 15, 5],
            4: [15, 20, 16, 55],
            5: [17, 5, 18, 40],
            6: [19, 20, 21, 45]
        }
        第一周第一天 = datetime.fromtimestamp(
            get_week_info()['currentsemester']['begintime'] / 1000
        )

        所有课程的事件们 = [处理一门课程(课程) for 课程 in 纯纯课程列表]

        return sorted(
            flatten(所有课程的事件们),
            key=lambda x: x['begin']
        )


class Global(APIView):

    def get(self):


        def ignore_event(ev):
            name = ev['name']
            if name.startswith('研 '):
                return True
            if ('研究生' in name) and ('本科生' not in name):
                return True
            return False

        def wrap_event(ev):
            status = ev['status']
            try:
                status = {
                    'begin': '开始',
                    'end': '结束'
                }[status]
            except KeyError:
                pass
            today = datetime.combine(
                datetime.today().date(), datetime.min.time())

            return {
                'title': ev['name'].strip() + status,
                'date': wrap_date(today + timedelta(ev['remainingdays']))
            }

        events = get_events()

        return [wrap_event(ev) for ev in events if not ignore_event(ev)]


class Semester(APIView):

    def get(self):
        week_info = get_week_info()
        开学日期 = datetime.fromtimestamp(
            week_info['currentsemester']['begintime'] / 1000
        )
        学期名 = week_info['currentsemester']['name']
        校历第几周 = week_info['currentteachingweek']['name']
        return {
            'semester_name': 学期名,
            'semester_bagin': wrap_date(开学日期),
            'week_name': 校历第几周,
        }
