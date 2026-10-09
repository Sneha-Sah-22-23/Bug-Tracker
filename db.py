import sqlite3 as sql
from contextlib import contextmanager

@contextmanager
def db_connection(db_name):
    connection = sql.connect(db_name)
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

def init_db():
    with db_connection() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS 
            defects(
            ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            Title  TEXT NOT NULL,
            Module TEXT NOT NULL,
            Cause TEXT NOT NULL,
            Severity TEXT CHECK(Severity IN (('low'), ('medium'), ('high')))
            )""")


def add_defect(Title, Module, Cause, Severity):
    with db_connection() as cursor:
        cursor.execute("INSERT INTO defects (Title, Module, Cause, Severity) VALUES ( ?, ?, ?, ?)",
                       (Title, Module, Cause, Severity))
        

def list_defects():
    with db_connection() as cursor:
       cursor.execute("SELECT * FROM defects")
       return cursor.fetchall()   

def count_by_cause():
    with db_connection() as cursor:
       cursor.execute("SELECT Cause, COUNT(Cause) FROM defects GROUP BY Cause ORDER BY COUNT(Cause) DESC")
       return cursor.fetchall()

