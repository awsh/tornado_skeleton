
users = """
    CREATE TABLE users(
        id SERIAL NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        reset_key TEXT,
        reset_expires TIMESTAMP WITH TIME ZONE,
        PRIMARY KEY (id));"""
