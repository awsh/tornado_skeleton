import os

DATABASE_NAME = 'dn_name'
DATABASE_USER = 'db_user' 
DATABASE_PASSWORD = 'db_pass'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 5432


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
DEBUG = True
COOKIE_SECRET = "cookie secret"
XSRF_COOKIES = True
LOGIN_URL = "/login"
COMPRESS_RESPONSE = True

EMAIL_FROM_NAME = "from_name"
EMAIL_FROM_ADDRESS = "from_address"
EMAIL_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH, "email")
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "email_username"
EMAIL_PASSWORD = "email_password"

