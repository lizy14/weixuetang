import asyncio
from .Util import *

class Semester:
    def __init__(self, user):
        self.user = user

    @property
    async def courses(self):
        response = await wrapped_json('/learnhelper/{username}/courses' % {
            'username': self.user.username
        })
        return [
            Course(
                user = user,
                id   = _.courseId,
                name = _.coursename
            )
            for _ in response.courses
        ]
