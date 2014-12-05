import psycopg2.extras
import momoko
from handlers.base import Base

class Login(Base):
    def get(self):
        pass

    def post(self):
        pass

class Logout(Base):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")
