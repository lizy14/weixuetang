# -*- coding: utf-8 -*-
#
from datetime import datetime
from django.utils import timezone
import time


def wrap_time(d):
    return int(time.mktime(d.timetuple()))
