from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import requests
import flask
import sys
import os
import json

app = flask.Flask(__name__)

consumer_key=os.environ['TWITTER_API']
consumer_secret=os.environ['TWITTER_API_SECRET']
access_token=os.environ['TWITTER_ACCESS']
access_token_secret=os.environ['TWITTER_ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


# https://stackoverflow.com/questions/22469713/managing-tweepy-api-search
query = 'pork'
max_tweets = 2

results = auth_api.search(query, count = max_tweets)

tweets = []
for status in results:
    tweets.append(status.user.name + ": " + status.text)



@app.route('/') # Python decorator
def homepage():
    return flask.render_template(
            "index.html",
            tweets = tweets,
            tweets_len = len(tweets)
        ) 

app.run(
    debug=True,
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)