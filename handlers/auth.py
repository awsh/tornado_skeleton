import tornado
import momoko
import uuid
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


class Register(Base):
    def get(self):
        self.render("register.html")

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument("username", None)
        if not username:
            self.set_message("Username is required")
            self.redirect('/register')
            return
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        if not password:
            self.set_message("Password is required")
            self.redirect('/register')
            return
        password2 = self.get_argument("password2", None)
        if password2 != password:
            self.set_message("Passwords do not match")
            self.redirect("/register")
            return
        ip = self.request.remote_ip
        hashed_pw = self.CTX.encrypt(password)
        try:
            cursor = yield momoko.Op(
                self.db.execute,
                """INSERT INTO users
                (username, email, password)
                SELECT %s, %s, %s
                WHERE 
                    NOT EXISTS (
                        SELECT username FROM users WHERE username ILIKE %s
                    );""",
                (username, email, hashed_pw, username))
            if cursor.rowcount == 0:
                self.set_message("Username is unavailable")
                self.redirect('/register')
            else:
                self.set_message("Your account has been created")
                self.redirect('/')
        except:
            self.set_message("Something went wrong. :( Please try again.")
            self.redirect("/register")

class CheckUsername(Base):
    @tornado.gen.coroutine
    def get(self, username):
        cursor = yield momoko.Op(
            self.db.execute,
            """SELECT EXISTS (
                SELECT true FROM users
                WHERE username ILIKE %s);""",
            (username,))
        self.write(str(cursor.fetchone()[0]))

class ForgotPassword(Base):
    def get(self):
        self.render("forgot_password.html")

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument("username", None)
        if username:
            cursor = yield momoko.Op(
                self.db.execute,
                """SELECT email FROM users
                WHERE username ILIKE %s;""",
                (username,))
            if cursor.rowcount > 0:
                user_email = cursor.fetchone()[0]
                if user_email:
                    reset_key = uuid.uuid4().hex
                    cursor = yield momoko.Op(
                        self.db.execute,
                        """UPDATE users SET
                        reset_key = %s, 
                        reset_expires = (NOW() AT TIME ZONE 'utc' + interval '1 day')
                        WHERE username = %s
                        AND email = %s;""",
                        (reset_key, username, user_email))
                    self.email(to = user_email, 
                               subject='Password Reset',
                               template="password_reset",
                               reset_key=reset_key,
                               requested_ip=self.request.remote_ip)
                    self.set_message("Email has been sent.")
                else:
                    self.set_message("No email on file. Unable to reset password.")
            else:
                self.set_message("No user with that username.")
        else:
            self.set_message("You must enter a username.")
        self.redirect("/")


class ResetPassword(Base):
    @tornado.gen.coroutine
    def get(self, reset_key):
        cursor = yield momoko.Op(
            self.db.execute,
            """SELECT 
                CASE 
                    WHEN reset_key = %s 
                         and reset_expires > NOW() AT TIME ZONE 'utc' 
                         THEN true
                    ELSE false
                END
                FROM users;""",
            (reset_key,))
        good = cursor.fetchone()[0]
        if good:
            self.render("reset_password.html", reset_key=reset_key)
        else:
            self.set_message("Invalid Reset Key")
            self.redirect("/")

    @tornado.gen.coroutine
    def post(self, reset_key):
        password = self.get_argument("password", None)
        password2 = self.get_argument("password2", None)
        if password and password2:
            if password != password2:
                self.set_message("passwords do not match")
                self.redirect("/reset-password")
            else:
                hashed_pwd = self.CTX.encrypt(password)
                try:
                    cursor = yield momoko.Op(
                        self.db.execute,
                        """UPDATE users 
                        SET password = %s,
                        reset_key = null,
                        reset_expires = null
                        WHERE reset_key = %s;""",
                        (hashed_pwd, reset_key))
                    self.set_message("password reset successfully")
                except:
                    self.set_message("something went wrong. :( please try again.")
                self.redirect("/login")
