# To use this repository, you must follow these steps:

0.  Sign up for the twitter developer portal at https://developer.twitter.com
1.  Navigate to https://developer.twitter.com/en/portal/projects-and-apps and make a new app.
2.  Click on the key symbol after creating your project, and it will take you to your keys and tokens.
     If needed, you can regenerate your access token and secret.
3.  Sign up at https://spoonacular.com/food-api
4.  Locate your Spoonacular API key under Profile in the API console.
5.  Clone this repository by using git clone thttps://github.com/NJIT-CS490/project1-ete2.git
6.  Run the following in your terminal:
     sudo pip install tweepy
     (or) sudo pip3 install tweepy
     (or) pip install tweepy
     (or) pip3 install tweepy
7.  Install flask using the same process as above ([sudo] pip[3] install flask)
8.  Add your secret keys (from step 2) by making a new root-level file called twitter.env and populating it as follows.
     **** MAKE SURE THE FILE AND VARIABLES ARE NAMED THE EXACT SAME WAY AS DESCRIBED!!!***
     export KEY=''
     export KEY_SECRET=''
     export TOKEN=''
     export TOKEN_SECRET=''
9.  In the terminal, run 'source twitter.env'
10. Add your secret keys (from step 2) by making a new root-level file called spoon.env and populating it as follows.
    **** MAKE SURE THE FILE AND VARIABLE ARE NAMED THE EXACT SAME WAY AS DESCRIBED!!!***
    export KEY=''
11. In the terminal, run 'source spoon.env'
12. Run `python main.py`
13. If on Cloud9, preview templates/index.html. This should successfully render the HTML!




## Technical issues:

At one point, any change made to the CSS file was not picked up by the HTML file. The cause for this was, as far as I can tell, in the 
'href="{{ url_for('static', filename='./tstyle.css') }}' section of the html file. Upon changing the filename to simply '/tstyle.css',
changes to the CSS file were being picked up again (most of the time, as elaborated on in known issues). I changed the filename prefix
to './' originally as the files original name was simply 'style.css', which seems to have gotten mixed up sometimes with a likewise named
file in a different folder. I later decided to simply rename my current CSS file to 'tstyle.css', to avoid this confusion altogether, 
although I find it to be an odd problem and unscalable solution to make every CSS filename unique despite being in different folders.


I had some issue getting my spoonacular to work, the main problem being figuring out what the response was/why is was unsubscriptable.
Thanks to stackoverflow (https://stackoverflow.com/questions/34508981/response-object-is-not-subscriptable-python-http-post-request/34509116)
I reasonably quickly found converting it to json was the way to go.


Being quite inexperienced at web design (and design in general), I had the hardest time, by far, trying to
make the website at least bearable to look at. My biggest issue was figuring out how to divide the screen into
separate parts. I found the solution to this on stackoverflow at https://stackoverflow.com/questions/12284044/how-to-split-page-into-4-equal-parts,
which was very helpful. Unfortunately, one of the div's I set up was not working at all as intended, despite it
looking exactly like the others. It turned out that, from before I subdivided the window, I had used a 
different field of the same div where I set the fields position to relative, which would override
the position: absolute I added to the css file. As such, the box would move around as I zoomed in and out
in the browser. This was probably the simplest bug I had this entire project, as well as the hardest to solve.

## Known Issues:

When making changes in my CSS file, sometimes they go through, sometimes they do not. I have tried opening the preview in my browser and refreshing there, but this still does not
guarantee the changes made in the CSS file will be picked up. If I had more time, it is possible that I might have found the definite cause for this issue and resolved it,
which would allow me to experiment with the appearance of my webpage more, resulting in a (hopefully) prettier page.

The webpage deployed on heroku does not utilize the tstyle.css file at all when using https. Thanks to this reddit post I stumbled upon: 
https://www.reddit.com/r/Heroku/comments/fdsygw/css_not_loading_when_app_is_visited_via_https/
I found out that it does work fine when using http. I did not find a solution, and for the person who posted this thread the issue resolved itself
without any further action. Since it does seem to work fine using http, I hope that is sufficient.

## Improvements:

I use two calls to spoonacular to first get a random recipe with ID, then use the ID in a second call to get 
the ingredients. If I had more time, I would try to find a way to reduce these into one call that accomplishes
both goals, or find out with certainty that this is not possible, as right now I would wager there is a way 
to do this.