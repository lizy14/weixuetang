# -*- coding: utf-8 -*-
#


def update_fields(dst, ref, *args):
    for arg in args:
        if getattr(ref, arg, None):
            setattr(dst, arg, getattr(ref, arg))
