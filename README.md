### project1-ete2

## This program pulls tweets off twitter as long as they contain a specific query, and displays it in a browser using Flask, HTML and CSS







https://stackoverflow.com/questions/22469713/managing-tweepy-api-search
http://docs.tweepy.org/en/latest/api.html#search-methods



Technical issues:

At one point, any change made to the CSS file was not picked up by the HTML file. The cause for this was, as far as I can tell, in the 
'href="{{ url_for('static', filename='./tstyle.css') }}' section of the html file. Upon changing the filename to simply '/tstyle.css',
changes to the CSS file were being picked up again (most of the time, as elaborated on in known issues). I changed the filename prefix
to './' originally as the files original name was simply 'style.css', which seems to have gotten mixed up sometimes with a likewise named
file in a different folder. I later decided to simply rename my current CSS file to 'tstyle.css', to avoid this confusion altogether, 
although I find it to be an odd problem and unscalable solution to make every CSS filename unique despite being in different folders.

Known Issues:

When making changes in my CSS file, sometimes they go through, sometimes they do not. I have tried opening the preview in my browser and refreshing there, but this still does not
guarantee the changes made in the CSS file will be picked up. If I had more time, it is possible that I might have found the definite cause for this issue and resolved it,
which would allow me to experiment with the appearance of my webpage more, resulting in a (hopefully) prettier page.