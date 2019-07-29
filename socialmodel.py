from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEFINES THE USER OBJECT

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email= ndb.StringProperty()
    biography= ndb.TextProperty()
    location= ndb.StringProperty()
    #interests= ndb.PickleProperty()
    