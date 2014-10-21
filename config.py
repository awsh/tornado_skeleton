import os

DATABASE_NAME = 'db_name'
DATABASE_USER = 'db_user' 
DATABASE_PASSWORD = 'db_pass'
DATABASE_HOST = 'db_host'
DATABASE_PORT = 5432

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
DEBUG = True
COOKIE_SECRET = "cookie secret"
XSRF_COOKIES = True
LOGIN_URL = "/login"
COMPRESS_RESPONSE = True

