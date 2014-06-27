
import config

from passlib.context import CryptContext

import tornado.web

class Base(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        ''' returns username from cookie '''
        return self.get_secure_cookie("username")

    def render(self, template, **kwargs):
        ''' overrides the render function to add variables to all templates '''
        kwargs['config'] = config
        kwargs['user'] = self.get_current_user()
        super(Base, self).render(template, **kwargs)

    def get_crypt(self):
        CTX = CryptContext(
            schemes = ["bcrypt"],
            default = "bcrypt",
            all__vary_rounds = 0.1,
            bcrypt__default_rounds = 12,
            )
        return CTX