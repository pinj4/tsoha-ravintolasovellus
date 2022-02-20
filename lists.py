from flask import session
from db import db
from users import get_user_id
#from restaurants import get_restaurant_id

def create_list(name):
    username = session["username"]
    user_id = get_user_id(username)
    sql = "INSERT INTO lists (user_id, name) VALUES (:user_id, :name)"
    db.session.execute(sql, {"user_id":user_id, "name":name})
    db.session.commit()

def get_list_id(name):
    try:
        username = session["username"]
        user_id = get_user_id(username)
        sql = "SELECT id FROM lists WHERE name = :name AND user_id = :user_id"
        result = db.session.execute(sql,{"user_id":user_id, "name":name})
        return result.fethone()
    except:
        return False

def add_to_list(list_id, restaurant_id):
    #get_list_id(list_name)
    sql = "INSERT INTO list_content (list_id, restaurant_id) VALUES (:list_id, :restaurant_id)"
    db.session.execute(sql, {"list_id":list_id, "restaurant_id":restaurant_id})
    db.session.commit()

def get_list_content(list_id):
    sql = "SELECT restaurant_id FROM list_content WHERE list_id = :list_id"
    result = db.session.execute(sql, {"list_id":list_id}).fetchall()
    content = []
    for restaurant_id in result:
        sql = "SELECT id, name FROM restaurants WHERE restaurant_id = :restaurant_id"
        res = db.session.execute(sql, {"restaurant_id":restaurant_id})
        content.append(res)
    return content

def get_list_name(list_id):
    username = session["username"]
    user_id = get_user_id(username)
    #content = get_list_content(list_id)
    sql = "SELECT name FROM lists WHERE id = :list_id AND user_id = :user_id"
    result = db.session.execute(sql, {"list_id":list_id, "user_id":user_id}).fetchone()
    return result.name

def get_users_lists():
    try:
        username = session["username"]
        user_id = get_user_id(username)
        sql = "SELECT id, name FROM lists WHERE user_id = :user_id"
        result = db.session.execute(sql, {"user_id":user_id}).fetchall()
        return result
    except:
        return False




