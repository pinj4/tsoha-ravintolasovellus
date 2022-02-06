from werkzeug.security import check_password_hash, generate_password_hash
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

## TODO: check long enough password, unique username (signup)
## TODO: check right password and username (login)

#def user_id():
    #return session.get("username", 0)
def get_user(username):
    sql = "SELECT * FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user

def logout():
    del session["username"]

def admin(username):
    sql = "SELECT is_admin FROM users WHERE username = :username"
    result = db.session.execute(sql, {"username": username}).fetchone()
    if result == "t":
        return True
    if result == "f":
        return False