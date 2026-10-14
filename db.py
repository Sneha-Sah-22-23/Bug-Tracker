import sqlite3 as sql
from contextlib import contextmanager
from datetime import date

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

def init_db(cursor):
    cursor.execute(
         """CREATE TABLE IF NOT EXISTS 
        defects(
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Title  TEXT NOT NULL,
        Module TEXT NOT NULL,
        Cause TEXT NOT NULL,
        Severity TEXT CHECK(Severity IN (('low'), ('medium'), ('high'))),
        Created_at TEXT NOT NULL DEFAULT CURRENT_DATE,
        Fix_time REAL DEFAULT NULL
        )""")


def add_defect(cursor, Title, Module, Cause, Severity, Created_at=None , Fix_time=None):
    if Created_at is None:
        Created_at = date.today().isoformat()
    cursor.execute("INSERT INTO defects (Title, Module, Cause, Severity, Created_at, Fix_time) VALUES ( ?, ?, ?, ?, ?, ?)",
                   (Title, Module, Cause, Severity,  Created_at, Fix_time))
    
def list_defects(cursor):
    cursor.execute("SELECT * FROM defects")
    return cursor.fetchall()   

def count_by_cause(cursor):
    cursor.execute("SELECT Cause, COUNT(Cause) FROM defects GROUP BY Cause ORDER BY COUNT(Cause) DESC")
    return cursor.fetchall()

def fix_times(cursor):
    cursor.execute("SELECT Fix_time FROM defects WHERE Fix_time IS NOT NULL")
    return cursor.fetchall()

def count_by_defects_per_week(cursor):
    cursor.execute("SELECT strftime('%W', Created_at) AS Week, Count(*) FROM defects GROUP BY Week ORDER BY Week")
    return cursor.fetchall()

def severity_vs_fix_time(cursor):
    cursor.execute("SELECT CASE WHEN Severity = 'low' THEN 1 WHEN Severity = 'medium' THEN 2 WHEN Severity = 'high' THEN 3 END AS severity_score, Fix_time FROM defects WHERE Fix_time is NOT NULL")
    return cursor.fetchall()

def count_by_cause_and_module(cursor):
    cursor.execute("SELECT Cause, Module, COUNT(*) FROM defects GROUP BY Cause, Module")
    return cursor.fetchall()