import config
import urls
import momoko
import tornado.web

class Application(tornado.web.Application):
    def __init__(self):
        app_urls = urls.handler_urls
        
        settings = {
            "template_path"     : config.TEMPLATE_PATH,
            "static_path"       : config.STATIC_PATH,
            "debug"             : config.DEBUG,
            "compress_response" : config.COMPRESS_RESPONSE,
            "cookie_secret"     : config.COOKIE_SECRET,
            "xsrf_cookies"      : config.XSRF_COOKIES,
            "login_url"         : config.LOGIN_URL
            }

        self.db = momoko.Pool(
            dsn='dbname=%s user=%s password=%s host=%s port=%s' % (
                config.DATABASE_NAME,
                config.DATABASE_USER,
                config.DATABASE_PASSWORD,
                config.DATABASE_HOST,
                config.DATABASE_PORT),
                size=1)
        
        tornado.web.Application.__init__(self, app_urls, **settings)

