from flask import session
from db import db
from users import get_user

def get_all_restaurants():
    sql = "SELECT * FROM restaurants"
    result = db.session.execute(sql)
    return result.fetchall()

def get_restaurants_by_admin():
    username = session["username"]
    user = get_user(username)
    user_id = user.id
    sql = "SELECT * FROM restaurants WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def new_restaurant(name, city, address, category, price, description):
    #try: 
    username = session["username"]
    sql = "SELECT id FROM users WHERE username =:username"
    user_id = db.session.execute(sql, {"username":username}).fetchone()[0]

    sql = "INSERT INTO restaurants (user_id, name, city, address, category, price, description) VALUES (:user_id, :name, :city, :address, :category, :price, :description)"
    
    db.session.execute(sql, {"user_id":user_id, "name":name, "city":city,"address":address, "category":category, "price":price, "description":description})
    db.session.commit()

