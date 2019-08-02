import os
import webapp2
import data
import datetime

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
# email stuff
from google.appengine.api import app_identity
from google.appengine.api import mail
import datetime
# FUNCTION


def render_template(handler, file_name, template_values):
    path = os.path.join(os.path.dirname(__file__), 'templates/', file_name)
    handler.response.out.write(template.render(path, template_values))


def get_user_email():
    user = users.get_current_user()
    print(user)
    if user:
        return user.email()
    else:
        return None


def get_template_parameters():
    values = {}
    email = get_user_email()
    if email:
        values['learner'] = data.is_learner(email)
        values['expert'] = data.is_expert(email)
        values['logout_url'] = users.create_logout_url('/')
        values['upload_url'] = blobstore.create_upload_url('/profile-save')
        values['user'] = email
    else:
        values['login_url'] = users.create_login_url('/welcome')
        values['upload_url'] = blobstore.create_upload_url('/profile-save')
    return values


class MainHandler(webapp2.RequestHandler):
    def get(self):
            values = get_template_parameters()
            email = get_user_email()
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
        data.save_email(email)
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
                data.save_profile(email, name, biography, location, blob_info.key())
                self.redirect('/my-feed')


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


class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        user_id = self.request.get('id')
        user_profile = ndb.Key(urlsafe=user_id).get()

        blob_key = user_profile.profile_pic
        self.send_blob(blob_key)


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

#IMAGE MANIPULATION CODE ENDS HERE

#FEED CONTROLLER STARTS HERE

def InterestsMatch(userExpert):
   #This function checks to see that the user and expert have at least one interest in common
   current_user_interests =  data.get_user_interests(get_user_email())
   expert_user_interests = data.get_user_interests(userExpert.email)
   i = 0
   for interest in current_user_interests:
        if current_user_interests[interest] and expert_user_interests[interest]:
            return True
   return False

class FeedHandler(webapp2.RequestHandler):
    def get(self):   
       p = get_user_email()
       if p:
        values = get_template_parameters()
        profile = data.get_user_profile(p)
        neededlocation = profile.location
        values['image_url'] = '/profilepic?id=' + profile.key.urlsafe()
        expert_profiles = data.get_expert_profiles(neededlocation)
        expert_list = []
        for expert_profile in expert_profiles:
            if InterestsMatch(expert_profile):
                expert_profile.keyUrl = expert_profile.key.urlsafe()
                expert_list.append(expert_profile)
        values['available_experts'] = expert_list
        for expert in values['available_experts']:
            values['expimg']='/profilepic?id=' + expert.key.urlsafe()
        values['events'] = []
        events_key_list = data.get_user_profile(get_user_email()).events_list
        for events_key in events_key_list:
            event = events_key.get()
            values['events'].append(event)
        values['name'] = profile.name
        values['location'] = profile.location
        values['biography'] = profile.biography
        values['interests']= profile.interests
        render_template(self, 'profilefeed.html', values)
       else:
            self.redirect('/')


#FEED CONTROLLER ENDS HERE


#PROFILE SAVING CODE ENDS HERE

#INTERESTS CODE STARTS HERE

class SaveInterestsHandler(webapp2.RequestHandler):
    def post(self):
        interests = self.request.get('interests')
        values = get_template_parameters()
        values['interests'] = data.get_user_interests(get_user_email())
        for key in values['interests']:
            enabled = self.request.get(key)
            print(enabled)
            if enabled == key:
                values['interests'][key]=True
            else:
                values['interests'][key]=False
        new_interests = values['interests']
        data.save_interests(get_user_email(), new_interests)
        print(new_interests)
        self.redirect('/my-feed')

class EditInterestsHandler(webapp2.RequestHandler):
    def get(self):
        values = get_template_parameters()
        if get_user_email():
            if data.get_user_interests(get_user_email()):
                values['interests'] = data.get_user_interests(get_user_email())
                print(values['interests'])
                values['interests']= values['interests'].items()
                render_template(self, 'interest.html', values)
            else:
                interests={
                "Java":False,
                "Python":False,
                "JavaScript":False,
                "HTML":False,
                "CSS":False,
                "C#":False,
                "Industry Insight":False,
                "Internships and Experience":False,
                "AI":False,
                "Machine Learning":False,
                }

                render_template(self, 'interest.html', values)

#INTERESTS CODE ENDS HERE
#VIEWING EXPERT PROFILE CODE STARTS HERE


class ExpertProfileViewHandler(webapp2.RequestHandler):
    def get(self, name):
        values = get_template_parameters()

        profile = data.get_user_profile(data.get_user_email_by_name(name))
        print ">>>>Profile:"
        print profile
        if profile:
            values['image_url'] = '/profilepic?id=' + profile.key.urlsafe()
            values['profileid'] = profile.key.urlsafe()
            values['name'] = profile.name
            values['biography'] = profile.biography
            values['location'] = profile.location
            values['profile_pic'] = profile.profile_pic
            values['interests'] = data.get_user_interests(get_user_email())
            values['interests'] = values['interests'].items()
            values['email'] = get_user_email()
            values['events'] = []
            events_key_list = profile.events_list
            for events_key in events_key_list:
                event = events_key.get()
                values['events'].append(event)
        render_template(self, 'expert-from-student.html', values)


class SendMailHandler(webapp2.RequestHandler):
    def post(self):
        values = get_template_parameters()
        subject = "Hi! you have a new message from Hyperlink: " + self.request.get('subject')
        body = get_user_email() + " sent you: " + self.request.get('body')
        profile_id = self.request.get('profileid')
        profile = data.get_profile_by_id(profile_id)
        sender_address = 'NoReply@cssi-chat-2.appspotmail.com'
        mail.send_mail(sender_address, profile.email, subject, body)
        render_template(self, 'profilefeed.html', values)


class SaveEventHandler(webapp2.RequestHandler):
    def post(self):
        print("hello")
        email = get_user_email()
        name = self.request.get('name')
        description = self.request.get('description')
        date = datetime.datetime.strptime(self.request.get('date'), "%Y-%m-%d")
        data.save_event(email, name, date, description)
        self.redirect('/my-feed')


class SetUserHandler(webapp2.RequestHandler):
    def get(self):
        get_template_parameters()
        email = get_user_email()
        setvallea = data.is_learner(email)
        setvalexp = data.is_expert(email)
        if setvallea or setvalexp:
            print('EMAIL REC.')
            self.redirect('/my-feed')
        else:
            print('EMAIL UNREC.')
            self.redirect('/set-profile')


app = webapp2.WSGIApplication([
    ('/welcome', SetUserHandler),
    ('/set-profile', DefineHandler),
    ('/definition', SaveDefineHandler),
    ('/edit-profile-student', EditProfileHandler),
    ('/profile-save', SaveProfileHandler),
    ('/image', ImageHandler),
    ('/my-feed', FeedHandler),
    ('/interests', EditInterestsHandler),
    ('/interests-save', SaveInterestsHandler),
    ('/p/(.*)', ExpertProfileViewHandler),
    ('/send-mail', SendMailHandler),
    ('/img', ImageManipulationHandler),
    ('/create_event', SaveEventHandler),
    ('/profilepic', ViewPhotoHandler),
    ('/.*', MainHandler)
])
 