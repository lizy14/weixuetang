from wechat.wrapper import WeChatView
from userpage.models import Student
from django.http import HttpResponseForbidden
from WeLearn.settings import IGNORE_CODE_CHECK
from .baseview import *
import logging


class BaseAPI(BaseView):

    logger = logging.getLogger('API')

    def certificated(function=None):
        def wrapper(obj, *args, **kwargs):
            if not IGNORE_CODE_CHECK:
                if obj.request.session.get('openid', False):
                    student = Student.objects.get(
                        open_id=obj.request.session['openid'])
                else:
                    obj.check_input('code', 'state')
                    try:  # pragma: no cover
                        student, create = Student.objects.get_or_create(
                            open_id=WeChatView.open_id_from_code(obj.input['code']))
                        obj.request.session['code'] = obj.input['code']
                        obj.request.session['openid'] = student.open_id
                        obj.request.session.set_expiry(0)
                    except Exception as e:
                        obj.logger.exception(str(e))
                        return HttpResponseForbidden()
                obj.student = student
            else:  # pragma: no cover
                obj.check_input('student_id')
                student = Student.objects.get(pk=obj.input['student_id'])
                obj.student = student
            return function(obj, *args, **kwargs)
        wrapper._original = function
        return wrapper

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()  # pragma: no cover
        return self.api_wrapper(handler, *args, **kwargs)

    @property
    def body(self):
        return json.loads(self.request.body.decode() or '{}')

    @property
    def query(self):
        d = getattr(self.request, self.request.method, None)
        if d:
            d = d.dict()
        else:
            d = dict()
        d.update(self.request.FILES)
        return d

    @certificated
    def api_wrapper(self, func, *args, **kwargs):
        code = 0
        msg = ''
        result = json_handler = None
        try:
            result = func(*args, **kwargs)
            if result and isinstance(result, tuple) and len(result) > 1:  # pragma: no cover
                json_handler = result[1]
                result = result[0]
        except BaseError as e:
            code = e.code
            msg = e.msg
        except Exception as e:  # pragma: no cover
            code = -1
            msg = str(e)
            self.logger.exception(
                'Error occurred when requesting %s: %s', self.request.path, e)
        try:
            response = json.dumps({
                'code': code,
                'msg': msg,
                'data': result,
            }, default=json_handler)
        except:  # pragma: no cover
            self.logger.exception(
                'JSON Serializing failed in requesting %s', self.request.path)
            code = -1
            msg = 'Internal Error'
            response = json.dumps({
                'code': code,
                'msg': msg,
                'data': None,
            })
        return HttpResponse(response, content_type='application/json')

    def check_input(self, *keys):
        for k in keys:
            if k not in self.input:
                raise InputError('Field "%s" required' % (k, ))

import types
import logging
__logger__ = logging.getLogger(name=__name__)


class BindMeta(type):

    @staticmethod
    def bind_required(function=None):
        def wrapper(obj, *args, **kwargs):
            if obj.student.xt_id is None:
                raise UnbindError()
            return function(obj, *args, **kwargs)
        return wrapper

    def __new__(cls, name, bases, attrs):
        for k, v in attrs.items():
            if isinstance(v, types.FunctionType) and k.lower() in ('post', 'get', 'put', 'patch', 'delete'):
                attrs[k] = cls.bind_required(v)
        return type.__new__(cls, name, bases, attrs)


class APIView(BaseAPI, metaclass=BindMeta):
    pass
