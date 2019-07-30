from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEFINES THE USER OBJECT


class UserProfile(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    biography= ndb.TextProperty()
    location= ndb.StringProperty()
#<<<<<<< HEAD
    isLearner= ndb.BooleanProperty()
    isExpert = ndb.BooleanProperty()
    #interests= ndb.PickleProperty()
    
#=======
    interests= ndb.PickleProperty()
#>>>>>>> 1f3ed14c26d22caf618258047c219ce5c2ccce69
