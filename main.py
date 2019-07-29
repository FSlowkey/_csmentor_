import os
import #our own datastore py
import webapp2
import datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            profile = socialdata.get_user_profile(get_user_email())
            values['name'] = profile.name
        # user = users.get_current_user()
        # values = {}
        # if user:
            # values['logout_url'] = users.create_logout_url('/')
            # values['nickname'] = user.nickname()
        # else:
            # values['login_url'] = users.create_login_url('/')
        render_template(self, 'mainpage.html', values)


class ProfileEditHandler(webapp2.RequestHandler):
    def get(self):
        if not get_user_email():
            self.redirect('/')
        else:
            values = get_template_parameters()
            profile = socialdata.get_user_profile(get_user_email())
            values['name'] = profile.name
            values['description'] = profile.description
            render_template(self, 'profile-edit.html', values)

            
class ProfileSaveHandler(webapp2.RequestHandler):

    def post(self):
        email = get_user_email()
        if not email:
            self.redirect('/')
        else:
            error_text = ''
            name = self.request.get('name')
            description = self.request.get('description')
            if len(name) < 2:
                error_text += "name should be at least two characters.\n" 
            if len(name) > 20:
                error_text += 'name should be no more than 20 characters. \n'
            if len(name.split()) > 1:
                error_text += 'name should not have white spaces \n'
            if len(description) > 4000:
                error_text += 'description should be less than 4000 characters.\n'
                        for word in description.split():
                if len(word) > 50:
                    error_text += 'description contains words that are too long.\n'
                    break
            values = get_template_parameters()
            values['name'] = name
            values['description'] = description

            if error_text:
                values['errormsg'] = error_text
            else:
                socialdata.save_profile(email, name, description)
                values['successmsg'] = 'everything worked out fine'
            render_template(self, 'profile-edit.html', values)


class MainHandler(webapp2.RequestHandler):
    def get(self):
    render_template(self, 'mainpage.html', values)



app = webapp2.WSGIApplication([
    ('.*', MainHandler),
])