from handlers.base import Base

  
class Index(Base):
    def get(self):
        self.render('index.html')
