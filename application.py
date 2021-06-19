import sys
from dotenv import load_dotenv
from flask import Flask, render_template, session, redirect, url_for, request
from flask_dance.contrib.twitter import twitter

from userUtil import is_user_logged_in, create_user, authenticate_user, logout_user, find_other_users, confirm_user_exists, get_email_from_username, get_user_match_history
from GameController import is_user_in_game, load_board_from_ID, scan_users_games, create_board, delete_game_ID, update_board, close_game
from invites_controller import add_to_invite_list, load_player_invites, delete_from_invite_list
from socialUtil import load_socials
from email_controller import send_email_invite
from Utilities import get_query, create_database, create_tables, download_assets


application = Flask(__name__)
load_dotenv()
load_socials(application)

DEFAULT_BOARD_DIMENSION = 8

@application.route('/')
def index():
   print(session, file=sys.stderr)
   if is_user_logged_in():
      return redirect(url_for('home'))
   else:
      return render_template('index.html')

# displays the actual game board
@application.route('/game/<game_ID>', methods=['POST', 'GET'])
def game(game_ID):
   if is_user_logged_in():
      if is_user_in_game(int(game_ID), session['username']):
         board = load_board_from_ID(int(game_ID))
         team = 1
         if(board.getPlayer2() == session['username']):
            team = 2
         return render_template('game.html', board = board, team = team)
      else:
         return redirect(url_for('index'))

   else:
      return redirect(url_for('login'))

@application.route('/game/<game_ID>/<cmd>')
def command(game_ID, cmd):

   board = load_board_from_ID(int(game_ID))

   # move a piece
   if(cmd == 'move'):

      response = 'OK'

      piece_args = request.args.get('piece', None).split(',')
      piece = (int(piece_args[0]), int(piece_args[1]))
      cell_args = request.args.get('cell', None).split(',')
      cell = (int(cell_args[0]), int(cell_args[1]))
      print('Running command on game ' + game_ID +': ' + cmd + ' piece ' + request.args.get('piece', None) + ' to cell ' + request.args.get('cell', None), file=sys.stderr)

      # get team from username
      team = 1
      if(board.getPlayer2() == session['username']):
         team = 2

      print(board.checkMoves(piece, team), file=sys.stderr)
      if(not board.checkMoveLegal(piece, cell)):
         response = 'NOT OK'
      board.movePiece(piece, cell)
      update_board(board)

      return response, 200, {'Content-Type': 'text/plain'}

   # checks for a winner
   elif(cmd == 'check'):
      response = 'FALSE'

      print('Running command on game ' + game_ID +': ' + cmd, file=sys.stderr)

      winner = board.checkWinner()

      if(winner != 0):
         response = 'We have a winner!'
         close_game(board)
      

      return response, 200, {'Content-Type': 'text/plain'}
   

@application.route('/home', methods=['GET', 'POST'])
def home():
   if is_user_logged_in():
      games = scan_users_games(session['username'])
      invites = load_player_invites(session['username'])
      if request.method == 'GET':
         query = None
         return render_template('player_home.html', user_name=session['username'], games=games, invites= invites, results = None, history=get_user_match_history(session['username']))
      elif request.method == 'POST':
         form = request.form
         results = find_other_users(session['username'], form['user_search'])
         return render_template('player_home.html', user_name=session['username'], games=games, invites= invites, results = results, history=get_user_match_history(session['username']))
   else:
      return redirect(url_for('login'))

# information on how to play the game
@application.route('/tutorial')
def tutorial():
   return render_template('tutorial.html')

@application.route('/login', methods=['POST', 'GET'])
def login():
   
   if request.method == 'GET':
      return render_template('login.html', twitter_login=url_for('twitter.login'), facebook_login=url_for('facebook.login'))

   elif request.method == 'POST':

      # validate and check if the user exists
      if authenticate_user(request.form['username'], request.form['password']):
         return redirect(url_for('home'))

      # todo: if it doesn't exist, redirect back to login page with errors
      else:
         return render_template('login.html', twitter_login=url_for('twitter.login'), facebook_login=url_for('facebook.login'), error="Username or password invalid")

# after SSO is used, get the credentials
@application.route('/authorize')
def authorize():

   resp = twitter.get("account/verify_credentials.json")

   # facebook login
   if (resp == None):
      resp = facebook.get("/me")

   # twitter login
   else:
      if authenticate_user(username=resp.json()['screen_name'], sso=True):
         return redirect(url_for('home'))


@application.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))
   

@application.route('/signup', methods=['POST', 'GET'])
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

@application.route('/invite/send/<username>')
def invite(username):
   if is_user_logged_in():
      if confirm_user_exists(username) and username != session['username']:
         add_to_invite_list(username, session['username'])
         email = get_email_from_username(username)
         send_email_invite(email, session['username'], url_for('home'))
      return redirect(url_for('home'))
   else:
      return redirect(url_for('index'))

@application.route('/invite/accept/<username>')
def accept(username):
   if is_user_logged_in():
      if confirm_user_exists(username) and username != session['username'] and username in load_player_invites(session['username']):
         delete_from_invite_list(session['username'], username)
         board = create_board(session['username'], username, DEFAULT_BOARD_DIMENSION)
         return redirect(url_for('game', game_ID=board.getGame_ID()))
      else:
         return redirect(url_for('home'))
   else:
      return redirect(url_for('login'))

@application.route('/concede/<game_ID>')
def concede(game_ID):
   if is_user_logged_in():
      try:
         game_int = int(game_ID)
         if is_user_in_game(game_int, session['username']):
            board = load_board_from_ID(game_int)
            if session['username'] == board.getPlayer1():
               player = 1
            else:
               player = 2
            board.concede(player)
            close_game(board)
            delete_game_ID(game_int)
         return redirect(url_for('home'))
      except ValueError:
         return redirect(url_for('home'))
   else:
      return redirect(url_for('login'))
   

if __name__ == '__main__':
   application.debug = True

   if(not application.debug):
      create_database()
      create_tables()
      download_assets()

   application.run()