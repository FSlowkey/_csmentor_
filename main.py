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
    if user:  # this means that it's checking if the object user exists, exists = true
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    if get_user_email():
        values['logout_url'] = users.create_logout_url('/')
        values['upload_url'] = blobstore.create_upload_url('/upload')
        values['user'] = get_user_email()
    else:
        values['login_url'] = users.create_login_url('/')
    return values


# HANDLER
class MainHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'mainpage.html', values)


class EditStudentProfileHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        render_template(self, 'edit-profile-student.html', values)


class SaveInterestsHandler(webapp2.RequestHandler):
    def post(self):
        interests = []
        interests = self.request.post('interests')


#class SaveProfileHandler(webapp2.RequestHandler):
 #   def post(self):
  #      email = get_user_email()
   #     name = self.request.get('name')
    #    biography = self.request.get('biography')
     #   location =self.request.get('cityhidden')
      #  data.save_profile(email, name, biography, location)


class FileUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        values = get_template_parameters()
        print("in post")
        if get_user_email():
            print("got user email")
            upload_files = self.get_uploads()
            blob_info = upload_files[0]
            type = blob_info.content_type
            email = get_user_email()
            name = self.request.get('name')
            biography = self.request.get('biography')
            location =self.request.get('cityhidden')
            print("save attributes")

            # we want to make sure the upload is a known type.
            if type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                name = self.request.get('name')
                my_image = MyImage()
                my_image.name = name
                my_image.user = values['user']

                # image is a BlobKeyProperty, so we will retrieve the key for this blob
                my_image.image = blob_info.key()
                my_image.put()
                image_id = my_image.key.urlsafe()
                data.save_profile(email, name, biography, location, blob_info.key())
                print("redirect")
                self.redirect('/image?id=' + image_id)

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
    
        # we'll get the ID from the request
        image_id = self.request.get('id')
    
        # this will allow us to retrieve it from NDB
        my_image = ndb.Key(urlsafe=image_id).get()

        # we'll set some parameters and pass this to the template
        print("hello")
        values['image_id'] = image_id
        print(my_image)
        print(image_id)
        values['image_name'] = my_image.name
        render_template(self, 'profilefeed.html', values)

class MyImage(ndb.Model):
    name = ndb.StringProperty()
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
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(result)



#class EditInterestsHandler(webapp2.RequestHandler):
#    def get(self):
#        values = get_template_parameters()
#        if get_user_email():
#            #values[interests] = data.get_user_interests.get_user_email()
#            render_template(self, 'interests.html', values)
#
#   def post(self):
#        values = get_template_parameters()
#        i = 
#        if i.interests[skill] == checked
#        i.interests[skill] = False
#        interests = self.request.get("interests")
#        data.save_profile(interests)
# APP


app = webapp2.WSGIApplication([
    ('/edit-profile-student', EditStudentProfileHandler),
    #('/profile-save', SaveProfileHandler),
    ('/image', ImageHandler),
    ('/upload', FileUploadHandler),
    #('/interests', EditInterestsHandler),
    ('/img', ImageManipulationHandler),
    ('/.*', MainHandler)
])
