import asyncio
from .Util import *
from .Course import Course
import re

class Semester:
    def __init__(self, user):
        self.user = user

    @property
    async def curriculum(self):
        response = await wrapped_json('/curriculum/{username}'.format_map({
            'username': self.user.username
        }))
        assert(response['message'] == 'Success')
        return response['classes']

    @property
    async def courses(self):
        response = await wrapped_json('/learnhelper/{username}/courses'.format_map({
            'username': self.user.username
        }))
        def name(name):
            # remove trailing `(2016-2017秋季学期)`
            name = re.sub(r'\(\d+-\d+\w+\)$', '', name)
            # remove trailing `(1)` # TODO 课程同名的情形
            name = re.sub(r'\(\d+\)$', '', name)
            return name
        return [
            Course(
                user = self.user,
                id   = _['courseid'],
                name = name(_['coursename'])
            )
            for _ in response['courses']
        ]
