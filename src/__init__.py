from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates')
app.secret_key = 'super secret key :)'
app.config['SESSION_TYPE'] = 'filesystem'
Bootstrap(app)


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/game')
def game():
   return render_template('game.html')

@app.route('/tutorial')
def tutorial():
   return render_template('tutorial.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/signup')
def signup():
   return render_template('signup.html')

if __name__ == '__main__':
   app.debug = True
   app.run()