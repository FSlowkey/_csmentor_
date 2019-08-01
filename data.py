from socialmodel import UserProfile
from google.appengine.ext import ndb

# THIS IS THE FILE THAT DEALS WITH RETRIEVING A PROFILE AND SAVING THE EDITS

def save_interests(email, interests):
    p= get_user_profile(email)
    if p:
        p.interests = interests
        p.put()
    else:
        p.UserProfile(interests = interests)
        p.put()

def get_profile_by_name(name):
    q = UserProfile.query(UserProfile.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None

def save_profile(email, name, biography, location, profile_pic):
    p= get_user_profile(email)
    if p:
        p.name = name
        p.biography = biography
        p.location = location
        p.profile_pic = profile_pic
        p.put()
    else:
        p = UserProfile(email=email, name=name, biography=biography, location = location, profile_pic = profile_pic)
        p.put()


def save_email(email):
    p= get_user_profile(email)
    if p:
        p.put()
    else:
        p = UserProfile(email=email)
        p.put()

def define_stat(email, statusl, statuse):
    p= get_user_profile(email)
    p.isLearner = statusl
    p.isExpert = statuse
    p
    p.put()

def get_user_interests(email):
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

    user = get_user_profile(email)
    if user:
        if user.interests:
            return user.interests
        else:
            return interests
    else:
        return interests

def get_user_profile(email):
    q = UserProfile.query(UserProfile.email == email)
    results = q.fetch(1)
    for profile in results:
        return profile
    return None


def is_learner(email):
    p = get_user_profile(email)
    if p and p.isLearner:
        return True
    return False

def is_expert(email):
    p = get_user_profile(email)
    if p and p.isExpert:
        return True
    return False

def get_expert_profiles(location):
    q = UserProfile.query(UserProfile.location == location and UserProfile.isExpert == True)
    results = q.fetch()
    return results

def get_user_email_by_name(name):
    q = UserProfile.query(UserProfile.name == name)
    results = q.fetch(1)
    for profile in results:
        return profile.email


def get_profile_by_id(profile_id):
    profile_key = ndb.Key(urlsafe=profile_id)
    return profile_key.get()