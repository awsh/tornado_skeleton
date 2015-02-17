import handlers.index
import handlers.auth

handler_urls = [
    (r'/', handlers.index.Index),
    (r'/login', handlers.auth.Login),
    (r'/logout', handlers.auth.Logout),
    (r'/register', handlers.auth.Register),
    (r'/forgot-password', handlers.auth.ForgotPassword),
    (r'/reset-password/(?P<reset_key>[\w]+)', handlers.auth.ResetPassword),
]
