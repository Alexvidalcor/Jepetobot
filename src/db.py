
# Libraries used
import sqlite3
from sqlite3 import Error

# Global vars
mainTable = "Conversations"
con, cur = None, None

def TestDbConnection(dbFile):
    try:
        global con
        global cur
        con = sqlite3.connect(dbFile)
        cur = con.cursor()
        cur.execute(f"SELECT * from {mainTable} WHERE ID=1")
        print("Connection established succesfully")

    except Error as e:
        print(e)
        print("Connection NOT established\nFixings db connection...")
        OperateDb(con, cur)
        if cur.execute(f"SELECT * from {mainTable}"):
            print("Successful repair\nConnection established")
            con = sqlite3.connect(dbFile)
            cur = cur = con.cursor()
        else:
            print("Failed repair")
            raise Exception("Database was not created :(")


def OperateDb(con, cur, values=(), where=[], selection=[], tableName=mainTable, option="create", closeDB=False):

    if option == "create":
        print("Creating table...")
        cur.execute(f'''CREATE TABLE IF NOT EXISTS "{tableName}"
			("ID" INTEGER PRIMARY KEY AUTOINCREMENT,
			"UserName" TEXT,
			"Content" TEXT);''')
        con.commit()
        print("OK")

    if option == "select":
        if where == []:
            cur.execute(f"SELECT {selection} FROM {tableName}")
        else:
            cur.execute(
                f"SELECT {selection} FROM {tableName} WHERE {where[0]} = '{where[1]}'")

        queryData = cur.fetchall()
        return queryData

    if option == "insert":
        print("Inserting data...")
        cur.execute(f'''INSERT INTO "{tableName}" 
			(UserName,Content)
		VALUES (?,?);''', values)
        con.commit()
        print("OK")

    if option == "update":
        print("Updating data...")
        cur.execute(f'''UPDATE {tableName} SET 
                    UserName = ?,
                    Content = ?,
                WHERE {where[0]} = "{where[1]}"''', values)
        con.commit()
        print("OK")

    if option == "add":
        print("Adding new row...")
        cur.execute(f'''INSERT INTO "{tableName}" 
			(UserName, Content)
			VALUES(?,?);''', values)
        con.commit()
        print("OK")

    if option == "delete":
        print("Deleting row...")
        cur.execute(
            f'''DELETE FROM {tableName} WHERE {where[0]} = "{where[1]}"''')
        con.commit
        print("OK")

    if closeDB == True:
        con.close()




