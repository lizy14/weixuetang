import asyncio

from .Message import Message
from .File import File
from .Work import Work
from .Util import *

class Course:

    def __init__(self, user, id, name=None):
        self.id = id
        self.name = name
        self.user = user

    @property
    async def works(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/assignments' % {
            'username': self.user.username,
            'courseid': self.id
        })
        return [
            Work(
                user       = user,
                id         = _.sequencenum,
                title      = _.title,
                detail     = _.detail,
                start_time = _.startdate,
                end_time   = _.duedate,
                completion = 0 # TODO
                # TODO grading
            )
            for _ in response.assignments
        ]

    @property
    async def messages(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/notices' % {
            'username': self.user.username,
            'courseid': self.id
        })
        return [
            Message(
                user      = user,
                id        = _.sequencenum,
                title     = _.title,
                date      = _.publishtime
                detail    = _.content
            )
            for _ in response.notices
        ]

    @property
    async def files(self):
        response = await wrapped_json('/learnhelper/{username}/courses/{courseid}/documents' % {
            'username': self.user.username,
            'courseid': self.id
        })
        return [
            File(
                user = user,
                id   = _.sequencenum,
                name = _.title,
                title= _.explanation,
                size = _.size,
                date = _.updatingtime,
                url  = _.url
            )
            for _ in response.documents
        ]

    @property
    def dict(self):
        d = self.__dict__.copy()
        user = self.user.__dict__.copy()
        del user['session']
        d['user'] = user
        return d
