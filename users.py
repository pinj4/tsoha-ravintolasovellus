from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from flask import session
from db import db

def add_new_user(username, password, is_admin):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["username"] = user.username
            return True
        else:
            return False

def get_user(username):
    sql = "SELECT id, username, is_admin FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def get_user_id(username):
    user = get_user(username)
    return user.id

def is_admin():
    try:
        user = get_user(session["username"])
        return user.is_admin
    except:
        return False

def logout():
    del session["username"]

def check_user():
    try:
        if session["username"]:
            return True
    except:
        return False