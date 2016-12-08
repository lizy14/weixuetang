import asyncio

from .Message import Message
from .File import File
from .Work import Work
from .Util import *

import random


def get_completion(_):
    if _['scored']:
        return 2
    if _['state'] == "已经提交":
        return 1
    return 0


class Course:

    def __init__(self, user, id, name=None):
        self.id = id
        self.name = name
        self.user = user

    @property
    async def works(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/assignments'.format_map({
            'username': self.user.username,
            'courseid': self.id
        }))

        return [
            Work(
                user       = self.user,
                id         = _['assignmentid'],
                course_id  = self.id,
                title      = _['title'],
                detail     = _['detail'],
                start_time = from_stamp(_['startdate']),
                end_time   = from_stamp(_['duedate']),
                attachment = _['filename'],
                completion = get_completion(_),
                grading    = _['grade'],
                grading_comment = _['comment'],
                grading_author  = _['evaluatingteacher']
            )
            for _ in response['assignments']
        ]

    @property
    async def messages(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/notices'.format_map({
            'username': self.user.username,
            'courseid': self.id
        }))
        return [
            Message(
                user      = self.user,
                id        = _['noticeid'],
                title     = _['title'],
                date      = from_stamp(_['publishtime']),
                author    = _['publisher'],
                detail    = _['content']
            )
            for _ in response['notices']
        ]

    @property
    async def files(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/documents'.format_map({
            'username': self.user.username,
            'courseid': self.id
        }))
        return [
            File(
                user = user,
                id   = _['sequencenum'],
                name = _['title'],
                title= _['explanation'],
                size = _['size'],
                date = _['updatingtime'],
                url  = _['url']
            )
            for _ in response['documents']
        ]

    @property
    def dict(self):
        d = self.__dict__.copy()
        user = self.user.__dict__.copy()
        del user['session']
        d['user'] = user
        return d
