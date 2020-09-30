from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import requests
import flask
import os

app = flask.Flask(__name__)

consumer_key=os.environ['TWITTER_API']
consumer_secret=os.environ['TWITTER_API_SECRET']
access_token=os.environ['TWITTER_ACCESS']
access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
spoon_key = os.environ['SPOONACULAR_KEY']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

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
    dish_info.append(dish["readyInMinutes"])
    dish_info.append(recipe_json["servings"])
    dish_info.append(recipe_json["sourceUrl"])
    dish_info.append(recipe_list)
    
    return dish_info
    
    # --------------------------------------------------------------------------------------------
def get_recipe_placebo():
    
    recipe_list = ['1 cup uncooked white rice', '3 cups water', '1 tsp salt', '2 eggs, beaten', '1 cup Parmesan or Romano cheese', '1 Tbs fresh minced parsley or 1/2 Tbs dehydrated parsley', '1 cup plain breadcrumbs', 'oil for frying']
    
    dish_info = []
    dish_info.append("https://spoonacular.com/recipeImages/654735-556x370.jpg")
    dish_info.append("Party Rice Balls")
    dish_info.append("45")
    dish_info.append("24")
    dish_info.append("https://www.foodista.com/recipe/4FYGNZ3F/party-rice-balls")
    dish_info.append(recipe_list)
    
    return dish_info
# --------------------------------------------------------------------------------------------

@app.route('/') # Python decorator
def homepage():

    results = []
    try: 
        # find a random dish
        dish = get_recipe()
        
        query = dish["title"]
        # find a number of tweets related to the recipe we chose
        results = auth_api.search(q = query, count = max_tweets, lang = "en")
            
            
        dish_info = get_recipe_information(dish)
    except:
        dish_info = get_recipe_placebo()
        results = auth_api.search(q = dish_info[1], count = max_tweets, lang = "en")
    
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
        
    # in case the twitter api call returned nothing, fill a default tweet
    if(not tweets):
        tweet_information = []
        tweet_information.append("https://pbs.twimg.com/profile_images/1308010958862905345/-SGZioPb_normal.jpg")
        tweet_information.append("")
        tweet_information.append("")
        tweet_information.append("No tweets found related to " + dish_info[1])
        tweets.append(tweet_information)
        
    return flask.render_template(
            "index.html",
            tweet = tweets[0],
            tweets_len = len(tweets),
            dish_image = dish_info[0],
            dish_title = dish_info[1],
            dish_prep_time = dish_info[2],
            dish_servings = dish_info[3],
            dish_url = dish_info[4],
            dish_recipe = dish_info[5],
            dish_recipe_len = len(dish_info[5])
        ) 

app.run(
    debug=True,
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)