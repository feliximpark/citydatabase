# -*- coding: utf-8 -*-
# importing the necessary modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalogdb import Base, Cities, Items, User
from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, flash, make_response
from flask import session as login_session
import random
import string
import json
import requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
# importing the google client_secret
CLIENT_ID = json.loads(
  open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

# connecting the file to the database
engine = create_engine('sqlite:///citiesfinal.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# STARTING THE ROUTES
# calling the landing page
@app.route("/")
def landing_page():
    # hier sollen alle Kategorien plus die zehn letzten Items abgedruckt werden
    cities = session.query(Cities).all()
    items = session.query(Items).order_by(Items.id.desc()).all()[:9]
    return render_template("main.html", cities=cities, items=items,
                           login_session=login_session)


# routes for user-management
# calling the login-page
@app.route("/login")
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template("login.html", STATE=state)


# Creating route for login via Google-Account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Checking that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    # checking if user exists in our user-table
    user_id = getUserID(login_session['username'])
    if not user_id:
        user_id = createUser(login_session)
        print ("New user set")
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("You are now logged in as %s" % login_session['username'])
    return output


# Helper-methods for creating local-user-administration
def createUser(login_session):
    newUser = User(name=login_session['username'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(name=login_session['username']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(username):
    try:
        user = session.query(User).filter_by(name=username).one()
        return user.id
    except:
        return None


# Disconnection from google-Account
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s') % access_token
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print (response)
        return render_template("logout.html", login_session=login_session)
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user.',
                                  400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ROUTES FOR WORKING WITH CITITES
# showing the choosen city and its attractions
@app.route("/catalog/<cityname>/item")
def show_city(cityname):
    cities = session.query(Cities).all()
    city = session.query(Cities).filter_by(name=cityname).first()
    items = session.query(Items).filter_by(category_id=city.id).all()
    return render_template("cityitem.html", items=items, cities=cities,
                           city=city, login_session=login_session)


# WORKING WITH CITIES
# creating new city
@app.route("/newcity", methods=["GET", "POST"])
def new_city():
    if request.method == "POST":
        # checking if the form is filled out
        # than: creating an new city in the databasse
        if request.form["newcityname"]:
            city = request.form["newcityname"]
            city_instance = city.lower()
            city_instance = Cities(name=city, user_id=login_session["user_id"])
            session.add(city_instance)
            session.commit()
            # checking, if also an attraction is filled in
            # if yes: Write the attraction to the database,
            # using the city-id of the new inserted city
            if request.form["attraction"]:
                attraction = request.form["attraction"]
                new_description = request.form["description"]
                new_city = session.query(Cities).filter_by(name=city).first()
                city_id = new_city.id
                attraction_instance = attraction.lower().replace(" ", "_")
                attraction_instance = Items(name=attraction,
                                            description=new_description,
                                            category_id=city_id,
                                            user_id=login_session['user_id'])
                session.add(attraction_instance)
                session.commit()
                flash("Saved the new city %s!" % city)
                return redirect(url_for("landing_page"))
            else:
                flash("Saved the new city %s! No Attractions filled in." %
                      city)
                return redirect(url_for("landing_page"))
    else:
        return render_template("new_city.html", login_session=login_session)


# Deleting a city and all attractions
@app.route("/catalog/<city>/delete", methods=["GET", "POST"])
def delete_city(city):
    # before checking the request method, first check if the user is creator
    # of the city and is authorized to delete ist
    cityToDelete = session.query(Cities).filter_by(name=city).one()
    if cityToDelete.user_id != login_session['user_id']:
        return """<body><script>
                  alert('You are not authorized to delete this city.');
                  function reloc(){window.location=
                                'http://localhost:8080/catalog/%s/item'};
                  reloc();</script></body>""" % city

    if request.method == "POST":
        itemsToDelete = session.query(Items).filter_by(
                category_id=cityToDelete.id).all()
        for elem in itemsToDelete:
            session.delete(elem)
        session.delete(cityToDelete)
        session.commit()
        flash("The city %s and all its attraction are deleted!" % city)
        return redirect(url_for("landing_page"))
    else:
        return render_template("delete_city.html", city=city,
                               login_session=login_session)


# WORKING WITH ITEMS
# create an new item
@app.route("/catalog/<city>/newitem", methods=["GET", "POST"])
def new_item(city):
    choosen_city = session.query(Cities).filter_by(name=city).first()
    choosen_city_id = choosen_city.id
    if request.method == "GET":
        return render_template("new_item.html", city=choosen_city,
                               login_session=login_session)
    else:
        # reading infos about new attraction out of the form provided
        if request.form["newitem"]:
            new_item_name = request.form["newitem"]
            new_item_description = request.form["description"]
            new_item_instance = new_item_name.lower().replace(" ", "_")
            new_item_instance = Items(name=new_item_name,
                                      description=new_item_description,
                                      category_id=choosen_city_id,
                                      user_id=login_session['user_id'])
            session.add(new_item_instance)
            session.commit()
            flash("New attraction %s saved for %s" % (new_item_name,
                                                      choosen_city.name))
            return redirect(url_for("landing_page"))
        else:
            return "No new attraction filled in"


# Show description of a single item
@app.route("/catalog/<cityname>/<item>")
def show_item(cityname, item):
    description = session.query(Items).filter_by(name=item).one()
    return render_template("show_item.html", item=description,
                           login_session=login_session)


# editing an choosen item
@app.route("/catalog/<item>/edit", methods=["GET", "POST"])
def edit_item(item):
    itemToEdit = session.query(Items).filter_by(name=item).one()
    cities = session.query(Cities).all()
    # checking if user is creator of the attraction and
    # is authorized to change it
    if itemToEdit.user_id != login_session['user_id']:
        return """<script>alert('You are not authorized to edit this item');
        function reloc()
        {window.location='http://localhost:8080/catalog/%s/%s'};
        reloc()</script>""" % (itemToEdit.categories.name, itemToEdit.name)
    if request.method == "POST":
        if request.form["attraction"]:
            itemToEdit.name = request.form["attraction"]
            itemToEdit.description = request.form["description"]
            itemToEdit.category_id = request.form["category"]
            print (itemToEdit.category_id)
            session.add(itemToEdit)
            session.commit()
            flash("The attraction %s was edited!" % itemToEdit.name)
            return redirect(url_for("landing_page"))
    else:
        return render_template("edit_item.html", item=itemToEdit,
                               cities=cities, login_session=login_session)


# delete an attraction
@app.route("/catalog/<item>/delete)", methods=["GET", "POST"])
def delete_item(item):
    itemToDelete = session.query(Items).filter_by(name=item).one()
    # checking if user is the creator of the attraction to delete
    if itemToDelete.user_id != login_session['user_id']:
        print (itemToDelete.user_id)
        print (login_session['user_id'])
        return """<script>alert('You are not authorized to delete this item');
        function reloc()
        {window.location='http://localhost:8080/catalog/%s/%s'};
        reloc()</script>""" % (itemToDelete.categories.name, itemToDelete.name)
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        flash("Attraction %s was deleted!" % item)
        return redirect(url_for("landing_page"))
    else:
        return render_template("delete_item.html", item=itemToDelete,
                               login_session=login_session)


# the JSON-API
# doing a loop through all cities and all Attractions of the citys.
# Than storing the data in an Object (elem_items) and putting this object into
# a list.
# At the end, jsonify the list to get the result
@app.route("/catalog/json")
def json_api():
    all_elements = []
    all_cities = session.query(Cities).all()
    for elem in all_cities:
        all_items = session.query(Items).filter_by(category_id=elem.id).all()
        elem_items = {"name": elem.name,
                      "items": [i.serialize for i in all_items], "id": elem.id}
        all_elements.append(elem_items)
    return jsonify(categorys=all_elements)

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
