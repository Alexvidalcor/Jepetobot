# Libraries used
import sqlite3
from sqlite3 import Error

# Modules imported
from src.env.app_support import dbPath
from src.modules import logtool

def TestDbConnection():
    try:
        global con
        global cur
        con = sqlite3.connect(dbPath)
        cur = con.cursor()
        cur.execute(f"SELECT * from users WHERE ID=1")
        logtool.appLogger.info('Connection established succesfully')

    except Error as e:
        logtool.errorsLogger.error(f"¿First db init? After check database: {e}")
        logtool.appLogger.info('Connection NOT established, fixing db connection...')
        
        CreateTables(con)
        if cur.execute(f"SELECT * from users"):
            logtool.appLogger.info('Successful repair, connection established')
            con = sqlite3.connect(dbPath)
            cur = con.cursor()
        else:
            logtool.errorsLogger.critical(f"Failed DB fix, fatabase was not created")


def CreateTables(con):

    con.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    chat_id INTEGER NOT NULL)''')

    con.execute('''CREATE TABLE bot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    users_name TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    FOREIGN KEY (users_name) REFERENCES users (name),
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id))''')

    con.execute('''CREATE TABLE stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    users_name TEXT NOT NULL,
                    tokens INTEGER NOT NULL,
                    FOREIGN KEY (users_name) REFERENCES users (name))''')


def InsertUserMessage(username, content, chatid):

    query = "INSERT INTO users (name, content, chat_id) VALUES (?, ?, ?)"
    cur.execute(query, (username, content, chatid))
    con.commit()


def InsertAssistantMessage(username, content, chatid):

    query = "INSERT INTO bot (name, content, users_name, chat_id) VALUES (?, ?, ?, ?)"
    cur.execute(query, ("assistant", content, username, chatid))
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


def GetUserMessagesToReply(username, chatid):

    query = f'''
            SELECT *
            FROM users
            LEFT JOIN bot
            ON users.name = bot.users_name AND users.chat_id = bot.chat_id AND users.id = bot.id
            WHERE users.name = "{username}" AND users.chat_id = "{chatid}"
            LIMIT 6;
            '''


    cur.execute(query)

    return cur.fetchall()
