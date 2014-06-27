from handlers.index import Index
from handlers.login import Login
from handlers.logout import Logout
import tornado.web



handler_urls = [
                (r'/', Index),
                (r'/login', Login),
                (r'/logout', Logout)
               ]
        

