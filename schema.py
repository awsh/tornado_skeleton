
users = """
    CREATE TABLE users(
        id SERIAL NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        reset_id TEXT,
        reset_expires TIMESTAMP WITH TIMEZONE,
        PRIMARY KEY (id));"""
