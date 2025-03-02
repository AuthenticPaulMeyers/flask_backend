-- -- CREATE users TABLE
-- CREATE TABLE users(
--     id INTEGER,
--     firstname TEXT,
--     lastname TEXT,
--     email TEXT NOT NULL UNIQUE,
--     password,
--     PRIMARY KEY(id)
-- );

-- SELECT * FROM products WHERE NOT user_id = 1;
-- select * from users;

-- -- CREATE products TABLE
-- CREATE TABLE products (
--     id INTEGER,
--     user_id INTEGER,
--     name TEXT NOT NULL,
--     description TEXT,
--     price DECIMAL(5, 2) NOT NULL,
--     image BLOG,
--     PRIMARY KEY(id),
--     FOREIGN KEY(user_id) REFERENCES users(id)
-- );

select * from users;