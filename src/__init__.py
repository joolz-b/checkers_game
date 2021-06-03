import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for, request
from flask_dance.contrib.twitter import twitter
from userUtil import is_user_logged_in, create_user, authenticate_user, logout_user
from socialUtil import load_socials

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
      return render_template('login.html', twitter_login=url_for('twitter.login'))

   elif request.method == 'POST':

      # validate and check if the user exists
      if authenticate_user(request.form['username'], request.form['password']):
         return redirect(url_for('game'))

      # todo: if it doesn't exist, redirect back to login page with errors
      else:
         return redirect(url_for('login'))

@app.route('/authorize_twitter')
def authorize_twitter():

   resp = twitter.get("account/verify_credentials.json")

   print(resp, file=sys.stderr)
   if authenticate_user(username=resp.json()['screen_name'],sso=True):
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

      # todo: validate and check if user exists, if not, create the user
      if request.form['password'] == request.form['password_confirm']:
         create_user(request.form['username'], request.form['password'])


if __name__ == '__main__':
   app.debug = True
   app.run()