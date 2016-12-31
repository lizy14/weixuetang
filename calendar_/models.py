from django.db import models
from userpage.models import *
import json
from datetime import *
from ztylearn.Util import get_curriculum, get_week_info, parse_zty_stamp


class PersonalCalendar(models.Model):
    classes = models.TextField()  # JSON string, quick and dirty
    xt_id = models.CharField(max_length=32, null=True, db_index=True)

大节起止时分 = {
    1: [8, 0, 9, 35],
    2: [9, 50, 12, 15],
    3: [13, 30, 15, 5],
    4: [15, 20, 16, 55],
    5: [17, 5, 18, 40],
    6: [19, 20, 21, 45]
}


第一周第一天 = parse_zty_stamp(
    get_week_info()['currentsemester']['begintime']
)


def get_appointments(学号, 区间起点=None, 区间终点=None):

    def wrap_datetime(dt):
        return int(dt.timestamp())

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

            if(区间起点 and 区间终点):
                if 开始 < 区间起点 or 结束 > 区间终点:
                    continue

            该课程的事件们.append({
                'title': 课程名,
                'location': 地点,
                'begin': wrap_datetime(开始),
                'end': wrap_datetime(结束)
            })
        return 该课程的事件们

    cache, created = PersonalCalendar.objects.get_or_create(xt_id=学号)

    if created:
        纯纯课程列表 = get_curriculum(学号)
        cache.classes = json.dumps(纯纯课程列表)
        cache.save()
    else:
        纯纯课程列表 = json.loads(cache.classes)

    所有课程的事件们 = [处理一门课程(课程) for 课程 in 纯纯课程列表]

    return sorted(
        flatten(所有课程的事件们),
        key=lambda x: x['begin']
    )
