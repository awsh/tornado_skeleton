
import config
from passlib.context import CryptContext
import tornado.web
import functools
import mailer


class Base(tornado.web.RequestHandler):
    '''
        methods that apply to all other page handlers.
    '''
    CTX = CryptContext(
            schemes=["pbkdf2_sha512"],
            default="pbkdf2_sha512",
            all__vary_rounds=0.1,
            pbkdf2_sha512__default_rounds=8000,
            )

    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        ''' returns username from cookie. '''
        return self.get_secure_cookie("username")

    def check_admin(self):
        ''' implementation depends on site setup. '''
        return False

    def render(self, template, **kwargs):
        ''' overrides the render function to add variables to all templates '''
        kwargs['config'] = config
        kwargs['has_message'] = self.has_message
        kwargs['get_message'] = self.get_message
        super(Base, self).render(template, **kwargs)

    @classmethod
    def admin_required(self, method):
        '''
            decorates handler methods to allow only admin access.
        '''
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.check_admin():
                return method(self, *args, **kwargs)
            else:
                self.write("Access denied")
        return wrapper

    def set_message(self, message):
        self.set_secure_cookie("message", tornado.escape.url_escape(message))

    def has_message(self):
        message = self.get_secure_cookie("message")
        return True if message else False

    def get_message(self):
        if self.has_message():
            message = tornado.escape.url_unescape(
                self.get_secure_cookie("message"))
            self.clear_cookie("message")
        else:
            message = None
        return message

    def email(self, to, subject, template, **kwargs):
        '''
        adds mailer.send function to ioloop
        and calls it after 10 seconds
        '''
        loop = tornado.ioloop.IOLoop.current()
        loop.call_later(10,
                        mailer.send,
                        to=to,
                        subject=subject,
                        template=template,
                        **kwargs)
