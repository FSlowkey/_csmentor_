from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEFINES THE USER OBJECT


class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    biography= ndb.TextProperty()
    location= ndb.StringProperty()
    profile_pic=ndb.BlobKeyProperty()
    isLearner= ndb.BooleanProperty()
    isExpert = ndb.BooleanProperty()
    interests= ndb.PickleProperty()
