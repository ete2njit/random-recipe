To use this repository, you must follow these steps:

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




Technical issues:

At one point, any change made to the CSS file was not picked up by the HTML file. The cause for this was, as far as I can tell, in the 
'href="{{ url_for('static', filename='./tstyle.css') }}' section of the html file. Upon changing the filename to simply '/tstyle.css',
changes to the CSS file were being picked up again (most of the time, as elaborated on in known issues). I changed the filename prefix
to './' originally as the files original name was simply 'style.css', which seems to have gotten mixed up sometimes with a likewise named
file in a different folder. I later decided to simply rename my current CSS file to 'tstyle.css', to avoid this confusion altogether, 
although I find it to be an odd problem and unscalable solution to make every CSS filename unique despite being in different folders.


I had some issue getting my spoonacular to work, the main problem being figuring out what the response was/why is was unsubscriptable.
Thanks to stackoverflow, I reasonably quickly found converting it to json was the way to go.

Known Issues:

When making changes in my CSS file, sometimes they go through, sometimes they do not. I have tried opening the preview in my browser and refreshing there, but this still does not
guarantee the changes made in the CSS file will be picked up. If I had more time, it is possible that I might have found the definite cause for this issue and resolved it,
which would allow me to experiment with the appearance of my webpage more, resulting in a (hopefully) prettier page.