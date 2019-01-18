import os
from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers import Response
from werkzeug.utils import redirect
from db_manip import DbManip


class ResponseViews():
    def __init__(self):
        self.app_db = DbManip()
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)

    def render_template(self, template_name, **context):
        the_template = self.jinja_env.get_template(template_name)
        return Response(the_template.render(context), mimetype="text/html")

    def note_response(self, request):
        if request.method == "POST":
            self.app_db.add_announcement(request.form["title"], request.form["announcement"])
            return redirect("/notes")
        return self.render_template("note.html")

    def notes_response(self):
        announcements = self.app_db.get_announcements()
        return self.render_template("notes.html", announcements=announcements)

    def error_404(self):
        response = self.render_template('404.html')
        response.status_code = 404
        return response
