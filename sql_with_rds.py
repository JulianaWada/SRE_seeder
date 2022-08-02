from configparser import ConfigParser
import psycopg2
import os

DB_CONFIG_FILE = os.path.dirname(__file__) + '/database.ini'


def config(filename=DB_CONFIG_FILE, section='postgresql'):
    # create a parser
    parser = ConfigParser()

    #read the configuration
    parser.read(filename)

    # get the section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0] not found in the {1} file', format(section, filename))
    return db


def connect_to_rds():
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the postgresql database
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL Database Version:")
        cur.execute('SELECT version()')

        # fetch the data
        db_version = cur.fetchone()
        print(db_version)

        # close the connection
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')


def create_tables():
    # provide sql statements
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL
        ) 
        """,
        """
        CREATE TABLE accounts (
            account_id SERIAL PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL
        )
        """
    )

    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # execute commands one by one
        for command in commands:
            cur.execute(command)

        cur.close()

        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()