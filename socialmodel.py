from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEFINES THE USER OBJECT
class Event(ndb.Model):
    email= ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateProperty()
    description = ndb.TextProperty()
    cap = ndb.TextProperty()

class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    biography= ndb.TextProperty()
    location= ndb.StringProperty()
    profile_pic=ndb.BlobKeyProperty()
    isLearner= ndb.BooleanProperty()
    isExpert = ndb.BooleanProperty()
    interests= ndb.PickleProperty()
    events_list = ndb.KeyProperty(Event, repeated=True)
