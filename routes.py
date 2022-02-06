from flask import render_template, request, session, redirect
from os import getenv
from app import app
from db import db
import users
import restaurant

app.secret_key = getenv("SECRET_KEY")

## !!!!!!!!!!!!VAIHA DESCRIBTION ->>>> DESCRIPTION !!!!!!!!

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            user = users.get_user(username)
            if user.is_admin == True:
                return redirect("/admin_page")
            if user.is_admin == False:
                return redirect("/user_page")
            else:
                return render_template("error.html")
        else:
            return render_template("error.html")

    ## todo alerts

@app.route("/user_page", methods = ["GET", "POST"])
def user_page():
    restaurants = restaurant.get_all_restaurants()
    return render_template("user.html", restaurants = restaurants)
    

@app.route("/admin_page", methods =["GET", "POST"])
def admin_page():
    #username = session["username"]
    restaurants = restaurant.get_restaurants_by_admin()
    return render_template("admin.html", restaurants = restaurants)


@app.route("/add_restaurant", methods = ["GET", "POST"])
def add_restaurant():
    if request.method == "GET":
        return render_template("add_restaurant.html")
    if request.method == "POST":
        name = request.form.get("name")
        city = request.form.get("city")
        address = request.form.get("address")
        price = request.form.get("price")
        category = request.form.get("category")
        desc = request.form.get("desc")
        
        restaurant.new_restaurant(name, city, address, category, price, desc)

        return redirect("/admin_page")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup_user", methods = ["GET", "POST"])
def signup_user():
    if request.method == "GET":
        return render_template("signup_user.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    ## TODO: check password (väh. 5 kirjainta ja numero)
    ## TODO: rewrite password (to confirm)

        users.add_new_user(username, password, False)

        return redirect("/user_page")

@app.route("/signup_admin", methods = ["GET", "POST"])
def signup_admin():
    if request.method == "GET":
        return render_template("signup_admin.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users.add_new_user(username, password, True)
        return redirect("/admin_page")


