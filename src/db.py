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
        print("Connection established succesfully")
        
    except Error as e:
        print(e)
        print("Connection NOT established\nFixings db connection...")
        CreateTables(con)
        if cur.execute(f"SELECT * from users"):
            print("Successful repair\nConnection established")
            con = sqlite3.connect(dbPath)
            cur = con.cursor()
        else:
            print("Failed repair")
            raise Exception("Database was not created :(")


def CreateTables(con):

    con.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL)''')

    con.execute('''CREATE TABLE bot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_name INTEGER NOT NULL,
                    FOREIGN KEY (name) REFERENCES users (name))''')
    

def InsertUserMessage(username,content):

    query = "INSERT INTO users (name, content) VALUES (?, ?)"
    cur.execute(query, (username, content))
    con.commit()


def InsertAsistantMessage(username, content):

    # Crear la consulta INSERT INTO
    query = "INSERT INTO bot (name, content, user_name) VALUES (?, ?, ?)"

    # Ejecutar la consulta y pasar los valores del nuevo registro como parámetros
    cur.execute(query, ("assistant", content, username))

    # Guardar los cambios en la base de datos
    con.commit()

