
import psycopg2.extras
import momoko
from base import Base

  
class Index(Base):
    def get(self):
        self.write('index')