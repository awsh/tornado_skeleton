from handlers.base import Base
import tornado
  
class Index(Base):
    @tornado.gen.coroutine
    def get(self):
        x = yield self.db.execute("SELECT NOW();")
#        self.write(str(x.fetchone()))
        self.render('index.html')
