import config
import momoko

db = momoko.Pool(
        dsn='dbname=%s user=%s password=%s host=%s port=%s' % (
            config.DATABASE_NAME,
            config.DATABASE_USER,
            config.DATABASE_PASSWORD,
            config.DATABASE_HOST,
            config.DATABASE_PORT),
         size=1)
