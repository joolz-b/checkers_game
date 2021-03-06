import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.consumer import oauth_authorized

def load_socials(app):
  app.secret_key = 'super secret key :)'
  app.config['TWITTER_OAUTH_CLIENT_KEY'] = os.environ.get('TWITTER_OAUTH_CLIENT_KEY')
  app.config['TWITTER_OAUTH_CLIENT_SECRET'] = os.environ.get('TWITTER_OAUTH_CLIENT_SECRET')
  app.config["FACEBOOK_OAUTH_CLIENT_KEY"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_KEY")
  app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
  twitter_bp = make_twitter_blueprint()
  facebook_bp = make_facebook_blueprint()
  app.register_blueprint(facebook_bp, url_prefix="/login")
  app.register_blueprint(twitter_bp, url_prefix="/login")

@oauth_authorized.connect
def redirect_to_next_url(blueprint, token):
  blueprint.token = token
  return redirect(url_for('authorize'))