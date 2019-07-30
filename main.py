import os
import webapp2
import data

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb

# FUNCTION


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    email = get_user_email()
    if email:
        values['learner'] = data.is_learner(email)
        values['expert'] = data.is_learner(email)
        values['logout_url'] = users.create_logout_url('/')
        values['upload_url'] = blobstore.create_upload_url('/profile-save')
        values['user'] = email
    else:
        values['login_url'] = users.create_login_url('/')
    return values


class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'mainpage.html', values)


#PROFILE SETTING CODE STARS HERE

class DefineHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'areyouor.html', values)


class SaveDefineHandler(webapp2.RequestHandler):
    def post(self):
        print('testing')
        email = get_user_email()
        defineStat = self.request.get('defineStat')
        if defineStat == "isLearner":
            learnerStat = True
            expertStat = False
        elif defineStat == "isExpert":
            expertStat = True
            learnerStat = False
        data.define_stat(email,learnerStat,expertStat)
        self.response.out.write('hello?')
        self.redirect('/edit-profile-student')
        

        
#PROFILE SAVING CODE STARTS HERE

class EditProfileHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'edit-profile-student.html', values)

#IMAGE SAVING CODE STARTS HERE


class SaveProfileHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        values = get_template_parameters()
        if get_user_email():
            upload_files = self.get_uploads()
            blob_info = upload_files[0]
            type = blob_info.content_type
            
            defineStat = self.request.get('defineStat')
            email = get_user_email()
            name = self.request.get('name')
            biography = self.request.get('biography')
            location =self.request.get('cityhidden')

            if type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                name= self.request.get('name')
                my_image= MyImage()
                my_image.name = name
                my_image.user = values['user']

                my_image.image = blob_info.key()
                my_image.put()
                image_id = my_image.key.urlsafe()
            

                data.save_profile(email, name, biography, location, blob_info.key())
                self.redirect('/image?id=' + image_id)

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()

        image_id=self.request.get('id')
        my_image = ndb.Key(urlsafe=image_id).get()

        values['image_id'] = image_id
        values['image_url'] = images.get_serving_url(
            my_image.image, size=150, crop=True
        )
        values['image_name'] = my_image.name
        values['biography'] = self.request.get('biography')
        render_template(self, 'profilefeed.html', values)

class  MyImage(ndb.Model):
    name= ndb.StringProperty()
    image = ndb.BlobKeyProperty()
    user = ndb.StringProperty()

class ImageManipulationHandler(webapp2.RequestHandler):
      def get(self):
 
       image_id = self.request.get("id")
       my_image = ndb.Key(urlsafe=image_id).get()
       blob_key = my_image.image
       img = images.Image(blob_key=blob_key)
      
       print(img)
 
       modified = False
 
       h = self.request.get('height')
       w = self.request.get('width')
       fit = False
 
       if self.request.get('fit'):
           fit = True
 
       if h and w:
           img.resize(width=int(w), height=int(h), crop_to_fit=fit)
           modified = True
 
       optimize = self.request.get('opt')
       if optimize:
           img.im_feeling_lucky()
           modified = True
 
       flip = self.request.get('flip')
       if flip:
           img.vertical_flip()
           modified = True
 
       mirror = self.request.get('mirror')
       if mirror:
           img.horizontal_flip()
           modified = True
 
       rotate = self.request.get('rotate')
       if rotate:
           img.rotate(int(rotate))
           modified = True
 
       result = img
       if modified:
           result = img.execute_transforms(output_encoding=images.JPEG)
       print("about to render image")
       img.im_feeling_lucky()
       self.response.headers['Content-Type'] = 'image/png'
       self.response.out.write(img.execute_transforms(output_encoding=images.JPEG))




#PROFILE SAVING CODE ENDS HERE

app = webapp2.WSGIApplication([
    ('/set-profile', DefineHandler),
    ('/definition', SaveDefineHandler),
    ('/edit-profile-student', EditProfileHandler),
    ('/profile-save', SaveProfileHandler),
    ('/image', ImageHandler),
    ('/img', ImageManipulationHandler),
    ('/.*', MainHandler)
])
