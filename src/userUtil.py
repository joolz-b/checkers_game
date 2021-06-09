from flask import session
from Utilities import run_query, get_query
import sys, random, string

def is_user_logged_in():
  res = False

  if session.get('username') != None:
    res = True

  return res

def find_other_users(current_user, username_email_contains):
  matches = []
  result = get_query(f"select username FROM users where UPPER(username) LIKE(UPPER('%{username_email_contains}%')) OR email LIKE(UPPER('%{username_email_contains}%'))")
  for record in result:
    if record[0] != current_user:
      matches.append(record[0])
  return matches

def get_email_from_username(username):
  result = get_query(f"select email FROM users where username = '{username}'")
  for record in result:  
    email = record[0]
  return email

def confirm_user_exists(username):
  result = get_query(f"select username FROM users where username = '{username}'")
  exists = False
  if result:
    exists = True
  return exists

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

  # account exists in the database
  if user:
    session['username'] = user[0][0]
    res = True

  # if no account exists, but sso is used, create it
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