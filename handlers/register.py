from handlers.base import Base
import tornado
import momoko

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
                (username, password)
                SELECT %s, %s
                WHERE 
                    NOT EXISTS (
                        SELECT username FROM users WHERE username ILIKE %s
                    );""",
                (username, hashed_pw, username))
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
