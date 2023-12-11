# Libraries used
from sqlcipher3 import dbapi2 as sqlcipher

# Modules imported
from src.env.app_public_env import dbPath, dbName
from src.env.app_secrets_env import dbKey
from src.modules import logtool

def TestDbConnection():
    try:
        global con
        global cur
        con = sqlcipher.connect(dbPath + "/" + dbName)
        con.execute(f'pragma key={dbKey}')
        cur = con.cursor() 
        cur.execute(f"SELECT * from users WHERE ID=1")
        logtool.appLogger.info('Connection established succesfully')

    except Exception as e:
        logtool.errorsLogger.error(f"¿First db init? After check database: {e}")
        logtool.appLogger.info('Connection NOT established, fixing db connection...')
        CreateTables(con)
        if cur.execute(f"SELECT * from users"):
            logtool.appLogger.info('Successful repair, connection established')
            con = sqlcipher.connect(dbPath + "/" + dbName)
            con.execute(f'pragma key={dbKey}')
            cur = con.cursor()
        else:
            logtool.errorsLogger.critical(f"Failed DB fix, fatabase was not created")


def CreateTables(con):

    con.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    via TEXT NOT NULL,
                    date TEXT NOT NULL)
                ''')

    con.execute('''CREATE TABLE bot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    users_name TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    via TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (users_name) REFERENCES users (name),
                    FOREIGN KEY (chat_id) REFERENCES users (chat_id))
                ''')

    con.execute('''CREATE TABLE stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    users_name TEXT NOT NULL,
                    tokens_gpt INTEGER,
                    tokens_dalle INTEGER,
                    tokens_whisper INTEGER,
                    tokens_tts INTEGER,
                    tokens_vision INTEGER,
                    FOREIGN KEY (users_name) REFERENCES users (name))
                ''')


def InsertUserMessage(username, content, chatid, via, date):

    query = "INSERT INTO users (name, content, chat_id, via, date) VALUES (?, ?, ?, ?, ?)"
    cur.execute(query, (username, content, chatid, via, date))
    con.commit()


def InsertAssistantMessage(username, content, chatid, via, date):

    query = "INSERT INTO bot (name, content, users_name, chat_id, via, date) VALUES (?, ?, ?, ?, ?, ?)"
    cur.execute(query, ("assistant", content, username, chatid, via, date))
    con.commit()


def OperateStatsToken(username, numTokens, option="gptCheck"):

    if option == "gptCheck":
        cur.execute(f'SELECT * FROM stats WHERE users_name = "{username}"')
        return cur.fetchone()
    elif option == "gptInsert":
        cur.execute(
            "INSERT INTO stats (tokens_gpt, users_name, tokens_dalle, tokens_whisper, tokens_tts, tokens_vision) VALUES (?, ?, 0, 0, 0, 0);", (numTokens, username))
    elif option == "gptUpdate":
        cur.execute(f'UPDATE stats SET tokens_gpt = tokens_gpt + {numTokens} WHERE users_name = "{username}"')
    
    elif option == "dalleCheck":
        cur.execute(f'SELECT * FROM stats WHERE users_name = "{username}"')
        return cur.fetchone()
    elif option == "dalleInsert":
        cur.execute(
            f'INSERT INTO stats (users_name, tokens_dalle, tokens_gpt, tokens_whisper, tokens_tts, tokens_vision) VALUES ("{username}", 1, 0, 0, 0, 0)')
    elif option == "dalleUpdate":
        cur.execute(f'UPDATE stats SET tokens_dalle = tokens_dalle + 1 WHERE users_name = "{username}"')

    elif option == "whisperCheck":
        cur.execute(f'SELECT * FROM stats WHERE users_name = "{username}"')
        return cur.fetchone()
    elif option == "whisperInsert":
        cur.execute(
            "INSERT INTO stats (tokens_whisper, users_name, tokens_dalle, tokens_gpt, tokens_tts, tokens_vision) VALUES (?, ?, 0, 0, 0, 0);", (numTokens, username))
    elif option == "whisperUpdate":
        cur.execute(f'UPDATE stats SET tokens_whisper = tokens_whisper + {numTokens} WHERE users_name = "{username}"')

    elif option == "ttsCheck":
        cur.execute(f'SELECT * FROM stats WHERE users_name = "{username}"')
        return cur.fetchone()
    elif option == "ttsInsert":
        cur.execute(
            "INSERT INTO stats (tokens_tts, users_name, tokens_dalle, tokens_whisper, tokens_gpt, tokens_vision) VALUES (?, ?, 0, 0, 0, 0);", (numTokens, username))
    elif option == "ttsUpdate":
        cur.execute("UPDATE stats SET tokens_tts = ? WHERE users_name = ?",
                    (numTokens, username))

    elif option == "visionCheck":
        cur.execute(f'SELECT * FROM stats WHERE users_name = "{username}"')
        return cur.fetchone()
    elif option == "visionInsert":
        cur.execute(
            f'INSERT INTO stats (users_name, tokens_dalle, tokens_gpt, tokens_whisper, tokens_tts, tokens_vision) VALUES ("{username}", 1, 0, 0, 0, 0)')
    elif option == "visionUpdate":
        cur.execute(f'UPDATE stats SET tokens_vision = tokens_vision + 1 WHERE users_name = "{username}"')
        
    con.commit()


def GetUserMessagesToReply(username, chatid):

    query = f'''
            SELECT *
            FROM users
            LEFT JOIN bot
            ON users.name = bot.users_name AND users.chat_id = bot.chat_id AND users.id = bot.id
            WHERE users.name = "{username}" AND users.chat_id = "{chatid}"
            ORDER BY users.id DESC
            LIMIT 6;
            '''

    cur.execute(query)
    
    results = cur.fetchall()
    results.reverse()
 
    return results
