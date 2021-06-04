from flask import session
import pymysql
from databaseUtil import run_query, get_query

def is_user_logged_in():
  res = False

  if session.get('username') != None:
    res = True

  return res

# users can either login via internal accounts or external (facebook, twitter)
def authenticate_user(username=None, password=None, sso=False):

  res = False

  # check if account exists internally
  sql = "SELECT username FROM users WHERE username=%s AND password=%s;" % (username, password)
  user = get_query(sql)

  # user exists in the database
  if user != None:
    session['username'] = username
    res = True

  # if internal account, but sso is used, create it
  if sso and user == None:
    create_user(username, 'email@email.com', 'some random string')
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