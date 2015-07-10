
import config
import urls

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

import momoko
import psycopg2.extras

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()
    
    settings = {
        "template_path"     : config.TEMPLATE_PATH,
        "static_path"       : config.STATIC_PATH,
        "debug"             : config.DEBUG,
        "compress_response" : config.COMPRESS_RESPONSE,
        "cookie_secret"     : config.COOKIE_SECRET,
        "xsrf_cookies"      : config.XSRF_COOKIES,
        "login_url"         : config.LOGIN_URL
        }

    ioloop = tornado.ioloop.IOLoop.instance()
    
    app = tornado.web.Application(
            urls.handler_urls,
            **settings)

    app.db = momoko.Pool(
                dsn='dbname={} user={} password={} host={} port={}'.format(
                    config.DATABASE_NAME,
                    config.DATABASE_USER,
                    config.DATABASE_PASSWORD,
                    config.DATABASE_HOST,
                    config.DATABASE_PORT),
                cursor_factory=psycopg2.extras.RealDictCursor,
                size=1,
                ioloop=ioloop)
    future = app.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.start()

if __name__ == "__main__":
    main()
