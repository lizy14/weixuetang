from celery import current_app
from celery.app.control import Inspect
from dateutil import parser


def visit_requests(func):
    schedule = Inspect(app=current_app).scheduled()
    return [[func(item['request']) for item in v] for k, v in schedule.items()]


def is_equal(req, task, args, kwargs, options):
    if req['name'] == task.name and eval(req['args']) == list(args) and eval(req['kwargs']) == kwargs and (not (getattr(options, 'eta', False) and options['eta'] != parser.parse(req['eta']))):
        return True
    return False


def safe_apply_async(task, args=None, kwargs={}, **options):
    def check(req):
        nonlocal task, args, kwargs, options
        if is_equal(req, task, args, kwargs, options):
            raise
        return False
    try:
        visit_requests(check)
        task.apply_async(args, kwargs, **options)
    except:
        return


def revoke(task, args=None, kwargs={}, **options):
    def check(req):
        nonlocal task, args, kwargs, options
        if is_equal(req, task, args, kwargs, options):
            current_app.control.revoke(req['id'])
            return True
        return False
    res = visit_requests(check)
    return sum([sum(x) for x in res])
