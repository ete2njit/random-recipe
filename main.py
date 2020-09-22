from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
#from collections import Counter
import requests
import flask
import sys
import os
import random



app = flask.Flask(__name__)

consumer_key=os.environ['TWITTER_API']
consumer_secret=os.environ['TWITTER_API_SECRET']
access_token=os.environ['TWITTER_ACCESS']
access_token_secret=os.environ['TWITTER_ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


foods = ['Pork Chop', 'General Tso\'s Chicken', 'Pineapple Pizza', 'Sushi', 'Beef Stew', 'Chicken Noodle Soup', 'Pasta e fagioli', 'Brownies', 'Dumplings', 'Chicken Sandwhich']
# I am using an array to store tweets in case I want to eventually display more than one, 
# or simply to have a few tweets to choose at random from 
max_tweets = 1


@app.route('/') # Python decorator
def homepage():

    results = []
    # while the results list is empty, search for more tweets. This is to prevent the case where no tweets are found, resulting in an error
    while(not results):
        # pick a random recipe from our list
        query = random.choice(foods)
        # find a number of tweets related to the recipe we chose
        results = auth_api.search(q = query, count = max_tweets, lang = "en")
    
    # store all tweets in an array while formatting
    tweets = []
    for status in results:
        # store image, user, date, and contents seperately to organize better in html/css
        tweet_information = []
        tweet_information.append(status.user.profile_image_url)
        tweet_information.append(status.user.name)
        tweet_information.append(str(status.created_at))
        tweet_information.append(status.text)
        tweets.append(tweet_information)
        
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