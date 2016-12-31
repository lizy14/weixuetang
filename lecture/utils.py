# -*- coding: utf-8 -*-
#
import re


class regex(object):
    __slots__ = ['__re__', 'match']

    def __init__(self):
        super(regex, self).__init__()
        self.__re__ = re.compile(self.__doc__)
        self.match = None

    @property
    def re(self):
        return self.__re__

    def check(self, s):
        self.match = self.re.match(s)
        return self.match is not None

    def get(self):
        raise NotImplementedError


class FindTime(regex):
    r'(?P<label>(时\s*间|日\s*期)\s*[:：]\s*)(?P<time>.*)'

    def get(self):
        return {'time': self.match.group('time')}


class FindPlace(regex):
    r'(?P<label>(地\s*点|教\s*室)\s*[:：]\s*)(?P<place>.*)'

    def get(self):
        return {'place': self.match.group('place')}


class FindLecturer(regex):
    r'(?P<label>(演\s*讲\s*人)\s*[:：]\s*)(?P<lecturer>.*)'

    def get(self):
        return {'lecturer': self.match.group('lecturer')}


class FindTitle(regex):
    r'(?P<label>(演\s*讲\s*题\s*目)\s*[:：]\s*)(?P<title>.*)'

    def get(self):
        return {'title': self.match.group('title')}


class CheckTitle(regex):
    r'第\d+周（周.*）.*【.*】'

import sys
import inspect


class Parser(object):
    finder = [eval(m[0])() for m in inspect.getmembers(
        sys.modules[__name__], inspect.isclass) if m[1].__module__ == __name__ and m[1].__name__.startswith('Find')]

    @classmethod
    def parse_line(cls, s):
        for ins in cls.finder:
            if ins.check(s):
                return ins.get()
        return {}  # useless

    @classmethod
    def parse(cls, title, content):
        res = {}
        if not CheckTitle().check(title):
            return (title, res)
        for line in content.splitlines():
            res.update(cls.parse_line(line))
        if res.get('title', False) and len(res['title']) > 0:
            title = res['title']
        return (title, res)
