# Libraries used
import sqlite3
from sqlite3 import Error

# Modules imported
from main import *
from src.modules.app_support import dbPath


def TestDbConnection():
    try:
        global con
        global cur
        con = sqlite3.connect(dbPath)
        cur = con.cursor()
        cur.execute(f"SELECT * from users WHERE ID=1")
        appLogger.info('Connection established succesfully')

    except Error as e:
        errorsLogger.error(f"After check database: {e}")
        appLogger.info('Connection NOT established, fixing db connection...')
        
        CreateTables(con)
        if cur.execute(f"SELECT * from users"):
            appLogger.info('Successful repair, connection established')
            con = sqlite3.connect(dbPath)
            cur = con.cursor()
        else:
            errorsLogger.critical(f"Failed DB fix, fatabase was not created")


def CreateTables(con):

    con.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL)''')

    con.execute('''CREATE TABLE bot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    users_name TEXT NOT NULL,
                    FOREIGN KEY (users_name) REFERENCES users (name))''')

    con.execute('''CREATE TABLE stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    users_name TEXT NOT NULL,
                    tokens INTEGER NOT NULL,
                    FOREIGN KEY (users_name) REFERENCES users (name))''')


def InsertUserMessage(username, content):

    query = "INSERT INTO users (name, content) VALUES (?, ?)"
    cur.execute(query, (username, content))
    con.commit()


def InsertAsistantMessage(username, content):

    query = "INSERT INTO bot (name, content, users_name) VALUES (?, ?, ?)"

    cur.execute(query, ("assistant", content, username))

    con.commit()


def OperateStatsToken(username, numTokens, option="select"):

    if option == "select":
        cur.execute(f'''
            SELECT tokens
            FROM stats
            WHERE users_name = "{username}"
            ''')
        return cur.fetchall()[0][0]
    elif option == "insert":
        cur.execute(
            "INSERT INTO stats (tokens, users_name) VALUES (?, ?);", (numTokens, username))
    elif option == "update":
        cur.execute("UPDATE stats SET tokens = ? WHERE users_name = ?",
                    (numTokens, username))

    con.commit()
