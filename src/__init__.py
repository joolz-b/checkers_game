import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for, request
from flask_dance.contrib.twitter import twitter

from userUtil import is_user_logged_in, create_user, authenticate_user, logout_user
from socialUtil import load_socials
from databaseUtil import run_query, get_query

app = Flask(__name__)
load_dotenv()
load_socials(app)

@app.route('/')
def index():
   print(session, file=sys.stderr)
   return render_template('index.html')

# displays the actual game board
@app.route('/game')
def game():
   
   if is_user_logged_in():
      return render_template('game.html')

   else:
      return redirect(url_for('login'))
      
# information on how to play the game
@app.route('/tutorial')
def tutorial():
   return render_template('tutorial.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
   
   if request.method == 'GET':
      return render_template('login.html', twitter_login=url_for('twitter.login'), facebook_login=url_for('facebook.login'))

   elif request.method == 'POST':

      # validate and check if the user exists
      if authenticate_user(request.form['username'], request.form['password']):
         return redirect(url_for('game'))

      # todo: if it doesn't exist, redirect back to login page with errors
      else:
         return render_template('login.html', twitter_login=url_for('twitter.login'), facebook_login=url_for('facebook.login'), error="Username or password invalid")

# after SSO is used, get the credentials
@app.route('/authorize')
def authorize():

   resp = twitter.get("account/verify_credentials.json")

   # facebook login
   if (resp == None):
      resp = facebook.get("/me")

   # twitter login
   else:
      if authenticate_user(username=resp.json()['screen_name'], sso=True):
         return redirect(url_for('game'))


@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))
   

@app.route('/signup', methods=['POST', 'GET'])
def signup():

   if request.method == 'GET':
      return render_template('signup.html')

   elif request.method == 'POST':

      # check if account exists internally
      sql = "SELECT email FROM users WHERE email='"+request.form['email']+"'" 
      user = get_query(sql)

      # if no user account exists, make sure the passwords match, then create it
      if not user:
         if request.form['password'] == request.form['password-confirm']:
            create_user(request.form['username'], request.form['email'], request.form['password'])
            return redirect(url_for('login'))
         else:
            return render_template('signup.html', error='Passwords do not match')
      else:
         return render_template('signup.html', error='Account already exists for this email')


if __name__ == '__main__':
   app.debug = True
   app.run()