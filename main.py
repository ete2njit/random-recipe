from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import requests
import flask
import sys
import os
import random
import json

app = flask.Flask(__name__)

consumer_key=os.environ['TWITTER_API']
consumer_secret=os.environ['TWITTER_API_SECRET']
access_token=os.environ['TWITTER_ACCESS']
access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
spoon_key = os.environ['SPOONACULAR_KEY']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

# stores the selection of foods we randomly choose from to find a recipe and one (or more) tweet(s)
foods = ['Pork Chop', 'General Tso\'s Chicken', 'Pizza', 'Sushi', 'Beef Stew', 'Chicken Noodle Soup', 'Pasta e fagioli', 'Brownies', 'Dumplings']


# I am using an array to store tweets in case I want to eventually display more than one, 
# or simply to have a few tweets to choose at random from 
max_tweets = 1


# This function gets the dish object on which we base tweetfinding and the later recipe information finding
def get_recipe():
    # First, find a random recipe based on the query prompt
    
    link = "https://api.spoonacular.com/recipes/random?apiKey=" + spoon_key + "&number=1&sort=random" 
    response = requests.get(link)
    # https://stackoverflow.com/questions/34508981/response-object-is-not-subscriptable-python-http-post-request/34509116
    data = response.json()
    
    return data["recipes"][0]
    
    
    
    
def get_recipe_information(dish):
    # https://spoonacular.com/food-api/docs#Get-Recipe-Information
    link = "https://api.spoonacular.com/recipes/" + str(dish["id"]) + "/information?apiKey=" + spoon_key + "&includeNutrition=false"
    response = requests.get(link)
    recipe_json = response.json()
    recipe = recipe_json["extendedIngredients"]
    
    recipe_list = []
    
    for i in range(0, len(recipe)):
        recipe_list.append(recipe[i]["original"])
    
    
    dish_info = []
    dish_info.append(dish["image"])
    dish_info.append(dish["title"])
    dish_info.append(recipe_json["servings"])
    dish_info.append(recipe_json["sourceUrl"])
    dish_info.append(recipe_list)
    
    return dish_info
    
# --------------------------------------------------------------------------------------------
def get_recipe_placebo():
    
    recipe_list = ['3 apples', '3 tsps Dijon mustard', '2 garlic cloves chopped finely', '4 tsps honey', 'Juice of a lemon', '1 tbsp olive oil', '4 pork chops', 'Salt and pepper', '1 large white onion sliced into thin rings']
    
    dish_info = []
    dish_info.append("https://spoonacular.com/recipeImages/656729-312x231.jpg")
    dish_info.append("Pork Chop with Honey, Mustard and Apples")
    dish_info.append("2 servings")
    dish_info.append("https://www.place.com/recipe")
    dish_info.append(recipe_list)
    
    return dish_info
# --------------------------------------------------------------------------------------------

@app.route('/') # Python decorator
def homepage():

    results = []
    # while the results list is empty, search for more tweets. This is to prevent the case where no tweets are found, resulting in an error
    while(not results):
        # find a random dish
        dish = get_recipe()
        
        query = dish["title"]
        # find a number of tweets related to the recipe we chose
        results = auth_api.search(q = query, count = max_tweets, lang = "en")
        
        
    dish_info = get_recipe_information(dish)
    
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
            tweets_len = len(tweets),
            dish_image = dish_info[0],
            dish_title = dish_info[1],
            dish_servings = dish_info[2],
            dish_url = dish_info[3],
            dish_recipe = dish_info[4],
            dish_recipe_len = len(dish_info[4])
        ) 

app.run(
    debug=True,
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)