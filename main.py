from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
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
spoon_key = os.environ['SPOONACULAR_KEY']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

# stores the selection of foods we randomly choose from to find a recipe and one (or more) tweet(s)
foods = ['Pork Chop', 'General Tso\'s Chicken', 'Pizza', 'Sushi', 'Beef Stew', 'Chicken Noodle Soup', 'Pasta e fagioli', 'Brownies', 'Dumplings']


# I am using an array to store tweets in case I want to eventually display more than one, 
# or simply to have a few tweets to choose at random from 
max_tweets = 1

def get_recipe(query):
    # First, find a random recipe based on the query prompt
    
    # https://spoonacular.com/food-api/docs#Authentication
    # https://spoonacular.com/food-api/docs#Search-Recipes-Complex
    link = "https://api.spoonacular.com/recipes/complexSearch?apiKey=" + spoon_key + "&query=" + query + "&number=1"
    response = requests.get(link)
    # https://stackoverflow.com/questions/34508981/response-object-is-not-subscriptable-python-http-post-request/34509116
    data = response.json()
    
    dish = data["results"][0]
    
    # Next, we find the actual recipe for the dish
    # https://spoonacular.com/food-api/docs#Get-Recipe-Information
    link = "https://api.spoonacular.com/recipes/" + "656729" + "/information?apiKey=" + spoon_key + "&includeNutrition=false"
    response = requests.get(link)
    recipe_json = response.json()
    recipe = recipe_json["extendedIngredients"]
    
    recipe_list = []
    
    for i in range(0, len(recipe)):
        recipe_list.append(recipe[i]["original"])
    
    print(recipe_list)
    print()
    print(recipe_json["summary"])
    
    
    dish_info = []
    dish_info.append(dish["image"])
    dish_info.append(dish["title"])
    dish_info.append(recipe_json["summary"])
    dish_info.append(recipe_list)
    
    return dish_info
    
# --------------------------------------------------------------------------------------------
def get_recipe_placebo(query):
    
    recipe_list = ['3 apples', '3 tsps Dijon mustard', '2 garlic cloves chopped finely', '4 tsps honey', 'Juice of a lemon', '1 tbsp olive oil', '4 pork chops', 'Salt and pepper', '1 large white onion sliced into thin rings']
    
    recipe_summary = 'Pork Chop with Honey, Mustard and Apples might be just the main course you are searching for. This caveman, gluten free, dairy free, and primal recipe serves 4 and costs <b>$2.4 per serving</b>. One serving contains <b>353 calories</b>, <b>30g of protein</b>, and <b>13g of fat</b>. If you have honey, onion, salt and pepper, and a few other ingredients on hand, you can make it. From preparation to the plate, this recipe takes about <b>45 minutes</b>. Only a few people made this recipe, and 1 would say it hit the spot. All things considered, we decided this recipe <b>deserves a spoonacular score of 59%</b>. This score is solid. Try <a href="https://spoonacular.com/recipes/mashed-sweet-potatoes-pork-chop-with-cider-gravy-sauteed-apples-and-onions-749564">Mashed Sweet Potatoes, Pork Chop with Cider Gravy, Sauteed Apples and Onions</a>, <a href="https://spoonacular.com/recipes/honey-mustard-chicken-and-apples-296098">Honey-Mustard Chicken and Apples</a>, and <a href="https://spoonacular.com/recipes/honey-mustard-coleslaw-with-apples-167187">Honey-Mustard Coleslaw with Apples</a> for similar recipes.'
    
    dish_info = []
    dish_info.append("https://spoonacular.com/recipeImages/656729-312x231.jpg")
    dish_info.append("Pork Chop with Honey, Mustard and Apples")
    dish_info.append(recipe_summary)
    dish_info.append(recipe_list)
    
    return dish_info
    

@app.route('/') # Python decorator
def homepage():

    results = []
    # while the results list is empty, search for more tweets. This is to prevent the case where no tweets are found, resulting in an error
    while(not results):
        # pick a random recipe from our list
        query = random.choice(foods)
        
        dish_info = get_recipe_placebo(query)
        
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
            tweets_len = len(tweets),
            dish_info = dish_info,
            dish_info_length = len(dish_info)
        ) 

app.run(
    debug=True,
    port=int(os.getenv('PORT', 8080)),
    host=os.getenv('IP', '0.0.0.0')
)