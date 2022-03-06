from db import db
from flask import session
from users import get_user_id

#def check_rating(rating):
    #if rating >= 1 and rating <= 5:
        #return True
    #return False

def check_comment(comment):
    return len(comment) >= 1 and len(comment) <= 200

def add_review(rating, comment, restaurant_id):
    username = session["username"]
    user_id = get_user_id(username)
    is_comment = check_comment(comment)

    if not is_comment:
        sql = "INSERT INTO reviews (user_id, username, restaurant_id, rating) VALUES (:user_id, :username, :restaurant_id, :rating)"
        db.session.execute(sql, {"user_id":user_id, "username":username, "restaurant_id": restaurant_id, "rating":rating})
        db.session.commit()
    if is_comment:
        sql = "INSERT INTO reviews (user_id, username, restaurant_id, rating, comment) VALUES (:user_id, :username, :restaurant_id, :rating, :comment)"
        db.session.execute(sql, {"user_id":user_id, "username":username, "restaurant_id": restaurant_id, "rating":rating, "comment":comment})
        db.session.commit()

def get_reviews(restaurant_id):
    sql = "SELECT username, rating, comment FROM reviews WHERE restaurant_id = :restaurant_id"
    result = db.session.execute(sql, {"restaurant_id":restaurant_id})
    return result.fetchall()

def avg_rating(restaurant_id):
    sql = "SELECT AVG(rating), SUM(rating) FROM reviews WHERE restaurant_id = :restaurant_id"
    result = db.session.execute(sql, {"restaurant_id": restaurant_id}).fetchone()
    ratings_sum = result[1]
    average = result[0]
    if ratings_sum:
        return "%.2f" % average
    else:
        return "no ratings yet"

    