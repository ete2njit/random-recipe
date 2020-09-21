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
import random



app = flask.Flask(__name__)

consumer_key=os.environ['TWITTER_API']
consumer_secret=os.environ['TWITTER_API_SECRET']
access_token=os.environ['TWITTER_ACCESS']
access_token_secret=os.environ['TWITTER_ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


foods = ['Pork Chop', 'General Tso\'s Chicken', 'Pineapple Pizza', 'Sushi', 'Beef Stew', 'Chicken Noodle Soup', 'Pasta e fagioli']
max_tweets = 1


@app.route('/') # Python decorator
def homepage():

    # pick a random recipe from our list
    query = foods[random.randint(0, len(foods)-1)]
    # find a number of tweets related to the recipe we chose
    results = auth_api.search(q = query, count = max_tweets)
    
    # store all tweets in an array while formatting
    tweets = []
    for status in results:
        tweets.append(status.user.name + ", " + str(status.created_at) + '\n' + status.text )
        
    return flask.render_template(
            "index.html",
            food = query,
            tweet = tweets[0],
            tweets_len = len(tweets)
        ) 

app.run(
    debug=True,
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)