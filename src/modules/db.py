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
        cur.execute(f"SELECT * from user WHERE ID=1")
        logtool.appLogger.info('Connection established succesfully')

    except Exception as e:
        logtool.errorsLogger.error(f"¿First db init? After check database: {e}")
        logtool.appLogger.info('Connection NOT established, fixing db connection...')
        CreateTables(con)
        if cur.execute(f"SELECT * from user"):
            logtool.appLogger.info('Successful repair, connection established')
            con = sqlcipher.connect(dbPath + "/" + dbName)
            con.execute(f'pragma key={dbKey}')
            cur = con.cursor()
        else:
            logtool.errorsLogger.critical(f"Failed DB fix, fatabase was not created")


def CreateTables(con):

    con.execute('''CREATE TABLE user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    via_input TEXT NOT NULL,
                    via_output TEXT NOT NULL,
                    date TEXT NOT NULL)
                ''')

    con.execute('''CREATE TABLE bot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    via_input TEXT NOT NULL,
                    via_output TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (user_name) REFERENCES user (name),
                    FOREIGN KEY (chat_id) REFERENCES user (chat_id))
                ''')

    con.execute('''CREATE TABLE stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    tokens_gpt INTEGER,
                    tokens_dalle INTEGER,
                    tokens_whisper INTEGER,
                    tokens_tts INTEGER,
                    tokens_vision INTEGER,
                    FOREIGN KEY (user_name) REFERENCES user (name))
                ''')


def InsertUserMessage(username, content, userId, chatId, viaInput, viaOutput, date):

    query = "INSERT INTO user (name, content, user_id, chat_id, via_input, via_output, date) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (username, content, userId, chatId, viaInput, viaOutput, date))
    con.commit()


def InsertAssistantMessage(content, username, userId, chatId, viaInput, viaOutput, date):

    query = "INSERT INTO bot (name, content, user_name, user_id, chat_id, via_input, via_output, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, ("assistant", content, username, userId, chatId, viaInput, viaOutput, date))
    con.commit()


def OperateStatsToken(username, userId, numTokens, option="gptCheck"):

    if option == "gptCheck":
        cur.execute(f'SELECT * FROM stats WHERE user_id = "{userId}"')
        return cur.fetchone()
    elif option == "gptInsert":
        cur.execute(
            "INSERT INTO stats (tokens_gpt, user_name, user_id, tokens_dalle, tokens_whisper, tokens_tts, tokens_vision) VALUES (?, ?, ?, 0, 0, 0, 0);", (numTokens, username, userId))
    elif option == "gptUpdate":
        cur.execute(f'UPDATE stats SET tokens_gpt = tokens_gpt + {numTokens} WHERE user_id = "{userId}"')
    
    elif option == "dalleCheck":
        cur.execute(f'SELECT * FROM stats WHERE user_id = "{userId}"')
        return cur.fetchone()
    elif option == "dalleInsert":
        cur.execute(
            f'INSERT INTO stats (user_name, user_id, tokens_dalle, tokens_gpt, tokens_whisper, tokens_tts, tokens_vision) VALUES ("{username}",{userId}, 1, 0, 0, 0, 0)')
    elif option == "dalleUpdate":
        cur.execute(f'UPDATE stats SET tokens_dalle = tokens_dalle + 1 WHERE user_id = "{userId}"')

    elif option == "whisperCheck":
        cur.execute(f'SELECT * FROM stats WHERE user_id = "{userId}"')
        return cur.fetchone()
    elif option == "whisperInsert":
        cur.execute(
            "INSERT INTO stats (tokens_whisper, user_name, user_id, tokens_dalle, tokens_gpt, tokens_tts, tokens_vision) VALUES (?, ?, ?, 0, 0, 0, 0);", (numTokens, username, userId))
    elif option == "whisperUpdate":
        cur.execute(f'UPDATE stats SET tokens_whisper = tokens_whisper + {numTokens} WHERE user_id = "{userId}"')

    elif option == "ttsCheck":
        cur.execute(f'SELECT * FROM stats WHERE user_id = "{userId}"')
        return cur.fetchone()
    elif option == "ttsInsert":
        cur.execute(
            "INSERT INTO stats (tokens_tts, user_name, user_id, tokens_dalle, tokens_whisper, tokens_gpt, tokens_vision) VALUES (?, ?, ?, 0, 0, 0, 0);", (numTokens, username, userId))
    elif option == "ttsUpdate":
        cur.execute("UPDATE stats SET tokens_tts = ? WHERE  user_id = ?",
                    (numTokens, userId))

    elif option == "visionCheck":
        cur.execute(f'SELECT * FROM stats WHERE  user_id = "{userId}"')
        return cur.fetchone()
    elif option == "visionInsert":
        cur.execute(
            f'INSERT INTO stats (user_name, user_id, tokens_dalle, tokens_gpt, tokens_whisper, tokens_tts, tokens_vision) VALUES ("{username}", {userId}, 1, 0, 0, 0, 0)')
    elif option == "visionUpdate":
        cur.execute(f'UPDATE stats SET tokens_vision = tokens_vision + 1 WHERE  user_id = "{userId}"')
        
    con.commit()


def GetUserMessagesToReply(userId, chatId):

    query = f'''
            SELECT *
            FROM user
            LEFT JOIN bot
            ON user.user_id = bot.user_id AND user.chat_id = bot.chat_id AND user.id = bot.id
            WHERE user.user_id = "{userId}" AND user.chat_id = "{chatId}"
            ORDER BY user.id DESC
            LIMIT 6;
            '''

    cur.execute(query)
    
    results = cur.fetchall()
    results.reverse()
 
    return results
