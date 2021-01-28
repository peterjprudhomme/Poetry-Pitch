# Poetry Pitch

Poetry Pitch is a content based recommendation system for poetry built around a flask application. It was created to help those who, like myself, are constantly on the lookout for new poets and poems to study and appreciate. Rather than reading through a poetry collection put together by someone else, this interactive site is designed to take in user feedback to make custom recommendations based on the poems YOU like with the goal of providing you with a variety of poems you are predicted to enjoy! All poems were web-scraped from the [Poetry Foundation website](https://www.poetryfoundation.org/).

## Navigating the files

Within the folder **flask_app** is the file **run.py**. To see the loaded web page on your local machine you must run this file from the command line. There is another folder, **flaskblog**, that contains all of the python, html, and css files that make up the webpages as well as the SQLite database file where the user info is stored. There is also the poem data csv file.

The **static** folder contains the css formatting file while the **templates** folder contains all the html files for each webpage.

## How to use this site (after running run.py from the command line)

First, you must create an account with a username and password and log in. 

Next, navigate to the Poem Recommendation page. Here you will see one poem along with two clickable links: 
- Like the poem
- Generate a random poem. 

In order to make sure the recommender has a variety of information about the poems you like, **you must first add 10 poems to your liked poem list** before the recommender starts to factor any in. This is to ensure your first few poems don't skew all subsequent recommendations. Before you reach 10 liked poems, all poems recommended will be randomly chosen from the database. After liking 10 poems, your first custom poem recommendation will appear on the webpage, along with a third button to generate another recommendation. 

From there simply sit back, crack your fingers, and enjoy some poetry!
