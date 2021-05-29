from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates')
Bootstrap(app)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/game')
def game():
   return render_template('game.html')

if __name__ == '__main__':
   app.debug = True
   app.run()