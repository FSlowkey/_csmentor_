from socialmodel import UserProfile


# THIS IS THE FILE THAT DEALS WITH RETRIEVING A PROFILE AND SAVING THE EDITS


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

def define_stat(email, statusl, statuse):
    p= get_user_profile(email)
    p.isLearner = statusl
    p.isExpert = statuse
    p.put()


def save_interest(email, interests):
    p = get_user_profile(email)
    if p:
        p.interests = interests
    else:
        p.UserProfile(interests = interests)
        p.put()


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

def get_user_interests(email):
    user = get_user_profile(email)
    if user:
        return user.interests
    else:
        return None
