import handlers
import tornado.web

handler_urls = [
                (r'/', handlers.Index),
                (r'/login', handlers.Login),
                (r'/logout', handlers.Logout)
               ]
        

