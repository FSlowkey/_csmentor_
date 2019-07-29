from google.appengine.ext import ndb

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email= ndb.StringProperty()
    biography= ndb.TextProperty()
    profile_picture_url= ndb.StringProperty()
    location= ndb.GeoPtProperty()
    interests= ndb.PickleProperty()
    