from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEFINES THE USER OBJECT

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email= ndb.StringProperty()
    biography= ndb.TextProperty()
    profile_picture_url= ndb.blobProperty()
    location= ndb.GeoPtProperty()
    interests= ndb.PickleProperty()
    