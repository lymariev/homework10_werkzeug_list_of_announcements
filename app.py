import os
from bson.errors import InvalidId
from werkzeug.wrappers import Request
from werkzeug.routing import Map, Rule
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.exceptions import HTTPException, NotFound
from views import ResponseViews


class Application():
    def __init__(self):
        self.app_response_views = ResponseViews()
        self.url_map = Map([
            Rule("/", endpoint="note"),
            Rule("/notes", endpoint="notes"),
        ])

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except (InvalidId, NotFound):
            return self.app_response_views.error_404()
        except HTTPException as err:
            return err

    def note(self, request):
        return self.app_response_views.note_response(request)

    def notes(self, request):
        return self.app_response_views.notes_response()

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def lofann(with_static=True):
    app = Application()
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
    return app


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = lofann()
    run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)
