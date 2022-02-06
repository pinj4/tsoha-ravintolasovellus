from flask import session
from db import db
from users import get_user

def get_all_restaurants():
    sql = "SELECT * FROM restaurants"
    result = db.session.execute(sql)
    return result.fetchall()

def get_restaurants_by_admin():
    #try:
    username = session["username"]
        #sql = "SELECT id FROM users WHERE username = :username"
        #user_id = db.session.execute(sql, {"username":username})
    user = get_user(username)
    user_id = user.id
    sql = "SELECT * FROM restaurants WHERE user_id = :user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()
    #except:
        #return False

def new_restaurant(name, city, address, category, price, describtion):
    #try: 
    username = session["username"]
    sql = "SELECT id FROM users WHERE username =:username"
    user_id = db.session.execute(sql, {"username":username}).fetchone()[0]

    sql = "INSERT INTO restaurants (user_id, name, city, address, category, price, describtion) VALUES (:user_id, :name, :city, :address, :category, :price, :describtion)"
    
    db.session.execute(sql, {"user_id":user_id, "name":name, "city":city,"address":address, "category":category, "price":price, "describtion":describtion})
    db.session.commit()
    
    #except:
        #return False
