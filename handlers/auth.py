import tornado
import psycopg2.extras
import momoko
from handlers.base import Base

class Login(Base):
    def get(self):
        if self.current_user:
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", next=self.get_argument("next", "/"))

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        remember_me = bool(self.get_argument("remember_me", False))
        next = self.get_argument("next", "/")

        try:
            cursor = yield momoko.Op(
                self.db.execute,
                """SELECT password
                FROM users 
                WHERE username ILIKE %s;""",
                (username,))
            if cursor.rowcount > 0:
                hashed_pw = cursor.fetchone()[0]
                if self.CTX.verify(password, hashed_pw):
                    if remember_me:
                        expires = None
                    else:
                        expires = 10
                    self.set_secure_cookie(
                        "username", username,
                        expires_days=expires)
                else:
                    self.set_message("Username or password is incorrect")
            else:
                self.set_message("Username or password is incorrect")
        except:
            self.set_message("Something went wrong. :( Please try again later.")
        self.redirect("/login?next=" + tornado.escape.url_escape(next))


class Logout(Base):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")
