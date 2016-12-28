from codex.apiview import BaseAPI


class FakeAPI(BaseAPI):

    def do_dispatch(self, *args, **kwargs):
        self.input = self.query or self.body
        handler = getattr(self, self.request.method.lower(), None)
        if not callable(handler):
            return self.http_method_not_allowed()
        return self.api_wrapper._original(handler, *args, **kwargs)
