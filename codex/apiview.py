from wechat.wrapper import WeChatView
from userpage.models import Student
from django.http import HttpResponseForbidden
from WeLearn.settings import IGNORE_CODE_CHECK
from .baseview import *


def certificated(function=None):
    def wrapper(obj, *args, **kwargs):
        if not IGNORE_CODE_CHECK:
            obj.check_input('code', 'state')  # TODO: actually state not used
            if obj.request.session.get('code', False) and obj.request.session.get('openid', False) and obj.input['code'] == obj.request.session['code']:
                student = Student.objects.get(
                    open_id=obj.request.session['openid'])
            else:
                try:
                    student = Student.objects.get(
                        open_id=WeChatView.open_id_from_code(obj.input['code']))
                    obj.request.session['code'] = obj.input['code']
                    obj.request.session['openid'] = student.open_id
                    obj.request.session.set_expiry(0)
                except:
                    return HttpResponseForbidden()
            obj.student = student
        else:
            student = Student.objects.all()[0]
            obj.student = student
        return function(obj, *args, **kwargs)
    return wrapper


def bind_required(function=None):
    def wrapper(obj, *args, **kwargs):
        try:
            assert(obj.student is not None)
            assert(obj.student.xt_id is not None)
        except:
            raise UnbindError()

        return function(obj, *args, **kwargs)
    return wrapper


class APIView(BaseView):

    logger = logging.getLogger('API')

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
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
            if result and isinstance(result, tuple) and len(result) > 1:
                json_handler = result[1]
                result = result[0]
        except BaseError as e:
            code = e.code
            msg = e.msg
            self.logger.exception(
                'Error occurred when requesting %s: %s', self.request.path, e)
        except Exception as e:
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
        except:
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
