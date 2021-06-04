from flask import session
from databaseUtil import run_query, get_query
import sys, random, string

def is_user_logged_in():
  res = False

  if session.get('username') != None:
    res = True

  return res

# users can either login via internal accounts or external (facebook, twitter)
def authenticate_user(username=None, password=None, sso=False):

  res = False

  # check if account exists internally
  sql = ''
  if not sso:
    sql = "SELECT username FROM users WHERE username='"+username+"' AND password='"+password+"'" 
  else:
    sql = "SELECT username FROM users WHERE username='"+username+"'"
  user = get_query(sql)

  # user exists in the database
  if user:
    session['username'] = user[0][0]
    res = True

  # if no internal account exists, but sso is used, create it
  if sso and not user:
    create_user(username, 'email@email.com', ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)))
    session['username'] = username
    res = True
  
  # otherwise no account exists

  return res

# creates a new user in the database
def create_user(username, email, password):
  sql = "insert into users(username, email, password) values('%s', '%s', '%s')" % (username, email, password)
  run_query(sql)

def logout_user():
  session.clear()