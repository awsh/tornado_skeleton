import handlers.index
import handlers.auth
import handlers.register

handler_urls = [
    (r'/', handlers.index.Index),
    (r'/login', handlers.auth.Login),
    (r'/logout', handlers.auth.Logout),
    (r'/register', handlers.register.Register)
]
