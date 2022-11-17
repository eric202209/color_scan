import psycopg2


def connect():
    """PostgreSQL Database server"""
    conn = None
    try:
        conn = psycopg2.connect(dbname="xxxx", user="xxxx", password="xxx", host="xxxx", port="xxxx")

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database setup')


if __name__ == '__main__':
    connect()