CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    name TEXT, 
    city TEXT,
    address TEXT,
    category TEXT,
    price INT,
    description TEXT
);

CREATE TABLE lists (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    name TEXT
);

CREATE TABLE list_content (
    list_id INT REFERENCES lists,
    restaurant_id INT REFERENCES restaurants
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INT REFERENCES restaurants,
    user_id INT REFERENCES users,
    username TEXT,
    rating INT,
    comment TEXT
);

