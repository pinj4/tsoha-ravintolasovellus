from flask import session
from db import db
from users import get_user_id

def get_all_restaurants():
    sql = "SELECT id, name, city, address, category, price, category, description FROM restaurants"
    result = db.session.execute(sql)
    return result.fetchall()

def get_restaurants_by_admin():
    username = session["username"]
    user_id = get_user_id(username)
    sql = "SELECT id, name, city, address, category, price, category, description FROM restaurants WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()


def new_restaurant(name, city, address, category, price, description):
    #try: 
    username = session["username"]
    user_id = get_user_id(username)

    sql = "INSERT INTO restaurants (user_id, name, city, address, category, price, description) VALUES (:user_id, :name, :city, :address, :category, :price, :description)"
    
    db.session.execute(sql, {"user_id":user_id, "name":name, "city":city,"address":address, "category":category, "price":price, "description":description})
    db.session.commit()

def get_restaurant(id):
    sql = "SELECT id, name, city, address, category, price, category, description FROM restaurants WHERE id = :id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_restaurant_id(name):
    sql = "SELECT id, name, city, address, category, price, category, description FROM restaurants WHERE name = :name"
    result = db.session.execute(sql, {"name":name})
    return result.fetchone()
    

