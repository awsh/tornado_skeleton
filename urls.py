import handlers.index
import handlers.auth

handler_urls = [
    (r'/', handlers.index.Index),
    (r'/login', handlers.auth.Login),
    (r'/logout', handlers.auth.Logout)
]
