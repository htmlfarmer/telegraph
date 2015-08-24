import datetime
import psycopg2

# EXPERIMENTAL

# PostgreSQL Client:
# http://www.postgresql.org/docs/current/static/reference-client.html

# PostgreSQL Server:
# http://www.postgresql.org/docs/current/static/runtime.html

# PostgreSQL Commands:
# http://www.postgresql.org/docs/current/static/reference.html

# PostgreSQL Data Types:
# http://www.postgresql.org/docs/current/static/datatype.html

conn = psycopg2.connect(dbname = 'orion',
                host = 'localhost',
                port = 5432,
                user = 'earthling',
                password = '') 

sql = conn.cursor()

def CREATE_TABLE(table, text):
    sql.execute("CREATE TABLE " + table + " (" + text + ");")

def INSERT(table, url, text):
    date = datetime.date.today()
    sql.execute("INSERT INTO %s (url, text, date) " \
        "VALUES (%s, %s, %s)" %(table, url, text, date))

def SELECT(table, url):
    sql.execute("SELECT * FROM %s WHERE url = %s" %(table, url))

def QUERY(text):
    sql.execute(text)

INSERT("main", "www.whoi.edu", "test")
print SELECT("main", "www.whoi.edu")

