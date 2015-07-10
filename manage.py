import config
import argparse
import subprocess
import sys
import psycopg2
import os
import datetime


def create_database():
    command = ["createdb", config.DATABASE_NAME]
    try:
        result = subprocess.call(command,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
    except AttributeError:  # if subprocess.DEVNULL unavailable use os.devnull
        with open(os.devnull, 'w') as DEVNULL:
            result = subprocess.call(command,
                                     stdout=DEVNULL,
                                     stderr=DEVNULL)

    if result != 0:
        sys.exit("Error: Database exists. Exiting...")
    else:
        print("Database {0} created.".format(config.DATABASE_NAME))
    populate_database()

def populate_database():
    try:
        con = psycopg2.connect(
            "dbname={} user={} password={} host={} port={}".format(
                config.DATABASE_NAME,
                config.DATABASE_USER,
                config.DATABASE_PASSWORD,
                config.DATABASE_HOST,
                config.DATABASE_PORT))
        cur = con.cursor()
        with open("schema.sql", "r") as f:
            cur.execute(f.read())
        con.commit()
        con.close()
        print("Database tables created successfully.")
    except:
        sys.exit("Table creation failed.")


def backup_database():
    filename = "{0}_{1}".format(
               config.DATABASE_NAME,
               datetime.datetime.now().strftime("%Y-%m-%d_%H:%M"))
    try:
        os.popen("pg_dump '{0}' | gzip > '{1}'.gz".format(config.DATABASE_NAME,
                                                          filename))
        print("Backup {0} completed.".format(filename))
    except:
        sys.exit("Error: Database backup failed.")


def restore_database(file_path):
    try:
        os.popen("gunzip -c {0} | psql {1}".format(file_path,
                                                   config.DATABASE_NAME))
        print("Restore completed successfully.")
    except:
        print("Error: Restore failed.")


def generate_cookie_secret():
    import base64
    import uuid
    print(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage script')
    parser.add_argument('--create-database', action="store_true",
                        help="creates database and tables")
    parser.add_argument('--populate-database', action="store_true",
                        help="applies schema to existing empty database")
    parser.add_argument('--backup-database', action="store_true",
                        help="backs up database to current directory")
    parser.add_argument('--restore-database', nargs=1, metavar='[BACKUP FILE]',
                        help="restores database from backup")
    parser.add_argument('--generate-cookie-secret', action="store_true",
                        help="generates cookie secret for use in config")
    args = parser.parse_args()
    if args.create_database:
        create_database()
    if args.populate_database:
        populate_database()
    if args.backup_database:
        backup_database()
    if args.generate_cookie_secret:
        generate_cookie_secret()
    if args.restore_database:
        restore_database(args.restore_database[0])
