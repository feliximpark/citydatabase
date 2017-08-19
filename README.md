# The Tourist-Attraction-App

The Tourist-Attraction-App is a database-app, that helps the user to find attractions in different cities. The database includes ten cities and ten attractions. The user can expand this database, inserting new cities and new attractions.
----------

## How to start
For working with the app, you have to use a Virtual Machine with Vagrant. Please use the vagrant-file included in this repository.

## How to create the database
Before starting the app for the first time, you have to fill the database with cities and attractions. For that you have to use the Python-files catalogdb.py and catalogpopulator.py. Start both files from your commandline. Catalogdb.py will create a sqlite-database called "citiesfinal.db". The database includes three tables called users, cities, items. Catalogpopulator.py will populate this database. You will get the message "DB populated" in the end.

## How to get the app running?
After creating the database, type in "python project.py" in your commandline. The programm will set up a localhost for the app.
*Go to http://localhost:8000 to start the app*

## What can I do with the app?
There is a different expierence for users who are logged-in and those who don´t. Users, who are not logged in, can only look at all the entries. But they can not change them. In the right upper corner a button tells you, if you are logged in or not.

## How can I log in?
For loggin-in you need a google-Account. By pressing the button "login" in the right upper corner of the screen, you will be passed to the google-login. After successfully logged in, you will be redirected on the starting page.

## What is the difference to the not-logged-in-status?
When logged-in, user can create new entries in the database. Every user can create an new city with new attractions. Also every user can make changes on his own entries - or even delete them. But: You cannot delete or change entries, another user has made.

## Credits
The descriptions of the entries in the database are parts of Wikipedia-articles. The whole project is inspired by the Full Stack Web Developer Nanodegree Program of Udacity an the included code-examples.