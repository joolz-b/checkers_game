from flask import session

def is_user_logged_in():
  res = False

  if session.get('username') != None:
    res = True

  return res

# users can either login via internal accounts or external (facebook, twitter)
def authenticate_user(username=None, password=None, sso=False):

  res = False
  # todo
  if True or sso:
    session['username'] = username
    res = True

  return res

def create_user(username):
  # todo
  return

def logout_user():
  session.clear()