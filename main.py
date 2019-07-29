import os
import socialdata
import webapp2


from google.appengine.ext.webapp import template
from google.appengine.api import users


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


class MainHandler(webapp2.RequestHandler):
    def get(self):
    render_template(self, 'mainpage.html', values)



app = webapp2.WSGIApplication([
    ('.*', MainHandler),
])