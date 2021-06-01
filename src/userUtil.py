from flask import session

def is_user_logged_in():
  res = False

  if session.get('username') != None:
    res = True

  return res

def authenticate_user(username, password):

  res = False
  # todo
  if True:
    session['username'] = username
    res = True

  return res

def create_user(username):
  # todo
  return

def logout_user():
  session.clear()