import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users


 #FUNCTION
 
def render_template(handler, file_name, template_values):
    path= os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))

def get_user_email():
    user = users.get_current_user()
    if user:  # this means that it's checking if the object user exists, exists = true
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
    else:
        values['login_url'] = users.create_login_url('/')
    return values


# HANDLER
class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'mainpage.html', values)

# APP


app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
])