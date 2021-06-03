import os
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

def load_socials(app):
  app.secret_key = 'super secret key :)'
  app.config['TWITTER_OAUTH_CLIENT_KEY'] = os.environ.get('TWITTER_OAUTH_CLIENT_KEY')
  app.config['TWITTER_OAUTH_CLIENT_SECRET'] = os.environ.get('TWITTER_OAUTH_CLIENT_SECRET')
  twitter_bp = make_twitter_blueprint()
  app.register_blueprint(twitter_bp, url_prefix="/login")