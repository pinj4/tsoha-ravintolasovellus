from flask import render_template, request, session, redirect, abort
from os import getenv
from app import app
from db import db
import users
import restaurant
import reviews
import lists

app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    admin = users.is_admin()
    return render_template("index.html", admin = admin)

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
            return render_template("error.html", message = "wrong username or password")

@app.route("/user_page", methods = ["GET"])
def user_page():
    if users.check_user():
        restaurants = restaurant.get_all_restaurants()
        users_lists = lists.get_users_lists()
        return render_template("user.html", restaurants = restaurants, lists = users_lists)
    else:
        return render_template("error.html", message= "you are not signed in")
    

@app.route("/admin_page", methods =["GET"])
def admin_page():
    if users.check_user():
        restaurants = restaurant.get_restaurants_by_admin()
        return render_template("admin.html", restaurants = restaurants)
    else:
        return render_template("error.html", message= "you are not signed in")


@app.route("/add_restaurant", methods = ["GET", "POST"])
def add_restaurant():
    if request.method == "GET":
        if users.check_user():
            return render_template("add_restaurant.html")
        else:
            return render_template("error.html", message= "you are not signed in")
    
    if request.method == "POST":
        if users.check_user():
            name = request.form.get("name")
            city = request.form.get("city")
            address = request.form.get("address")
            price = request.form.get("price")
            category = request.form.get("category")
            desc = request.form.get("desc")
        
            restaurant.new_restaurant(name, city, address, category, price, desc)

            return redirect("/admin_page")
        else:
            return render_template("error.html", message= "you are not signed in")
    
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

@app.route("/review_restaurant/<int:id>", methods = ["GET", "POST"])
def review_restaurant(id):
    if request.method == "GET":
        if users.check_user():
            restaurant_info = restaurant.get_restaurant(id)
            return render_template("review.html", restaurant = restaurant_info)
        else:
            return render_template("error.html", message= "you are not signed in")
    
    if request.method == "POST":
        if users.check_user():
            rating = request.form["rating"]
            comment = request.form["comment"]
            restaurant_info = restaurant.get_restaurant(id)

            reviews.add_review(rating, comment, id)
            return redirect("/restaurant_page/" + str(id))
        else:
            return render_template("error.html", message= "you are not signed in")
    

@app.route("/restaurant_page/<int:id>", methods = ["GET"])
def restaurant_page(id):
    if users.check_user():
        restaurant_info = restaurant.get_restaurant(id)
        reviews_info = reviews.get_reviews(id)
        avg_rating = reviews.avg_rating(id)
        admin = users.is_admin()

        return render_template("restaurant.html", restaurant = restaurant_info, reviews = reviews_info, 
        avg_rating = avg_rating, admin = admin)
    else:
        return render_template("error.html", message= "you are not signed in")
    

@app.route("/list_page/<int:id>", methods = ["GET", "POST"])
def list_page(id):
    if request.method == "GET":
        if users.check_user():
            content = lists.get_list_content(id)
            name = lists.get_list_name(id)

            return render_template("list.html", name = name, content = content, list_id = id)
        else:
            return render_template("error.html", message= "you are not signed in")
    
    if request.method == "POST":
        if users.check_user():
            restaurant_id = request.form["restaurant_id"]
            lists.delete_restaurant_from_lists(restaurant_id, id)
            return redirect("/list_page/" + str(id))
        else:
            return render_template("error.html", message= "you are not signed in")

@app.route("/add_to_list/<int:id>", methods = ["GET", "POST"])
def add_to_list(id):
    if request.method == "GET":
        if users.check_user():
            restaurant_info = restaurant.get_restaurant(id)
            users_lists = lists.get_users_lists()

            return render_template("add_to_list.html", restaurant = restaurant_info, lists = users_lists)
        else:
            return render_template("error.html", message= "you are not signed in")

    
    if request.method == "POST":
        if users.check_user():
            restaurant_id = id
            list_id = request.form["list_id"]

            if lists.check_already_in_lists(list_id, id):
                lists.add_to_list(list_id, restaurant_id)
                return redirect("/restaurant_page/" + str(id))
            else:
                return render_template("error.html", message = "restaurant is already added to this list")
        else:
            return render_template("error.html", message= "you are not signed in")


@app.route("/create_list", methods = ["GET", "POST"])
def create_list():
    if request.method == "GET":
        if users.check_user():
            return render_template("create_list.html")
        else:
            return render_template("error.html", message= "you are not signed in")
    
    if request.method == "POST":
        if users.check_user():
            name = request.form["name"]

            lists.create_list(name)
            return redirect("/user_page")
        else:
            return render_template("error.html", message= "you are not signed in")
    

@app.route("/delete_restaurant/<int:id>", methods = ["POST"])
def delete_restaurant(id):
    if request.method == "POST":
        if users.check_user():
            restaurant.delete_restaurant(id)
            return redirect("/admin_page")
        return render_template("error.html", message= "you are not signed in")

@app.route("/delete_review/<int:id>", methods = ["POST"])
def delete_review(id):
    if request.method == "POST":
        if users.check_user():
            restaurant_id = reviews.delete_review(id)
            return redirect("/restaurant_page/"+ str(restaurant_id))
        return render_template("error.html", message= "you are not signed in")
