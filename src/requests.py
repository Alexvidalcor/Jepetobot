# Python libraries
import openai

# Custom modules
from main import *
from src.permissions import UsersFirewall
from src.modules.app_support import openaiToken
from src.db import InsertUserMessage, InsertAsistantMessage

# Get OpenAI token
openai.api_key = openaiToken


def FormatCompletionMessages(cur, username, identity, promptUser):

    query = f'''
            SELECT *
            FROM users
            INNER JOIN bot
            ON users.name = bot.user_name
            WHERE users.name = "{username}"
            LIMIT 5
            '''

    cur.execute(query)

    results = cur.fetchall()

    conversationFormatted = [{"role": "system", "content": identity}]
    for row in results:
        conversationFormatted.append({"role": "user", "content": row[2]})
        conversationFormatted.append({"role": row[4], "content": row[5]})
    conversationFormatted.append({"role": "user", "content": promptUser})

    return conversationFormatted


def GenerateResponse(username, prompt, identity, temp):
    # Import latest connection object
    from src.db import con, cur

    InsertUserMessage(username, prompt)
    messagesFormatted = FormatCompletionMessages(cur, username, identity, prompt)

    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messagesFormatted,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=float(temp),
    )

    answerProvided = completions["choices"][0]["message"]["content"]

    InsertAsistantMessage(username, answerProvided)

    return answerProvided


@UsersFirewall
async def AiReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply the user message.
    await update.message.reply_text(GenerateResponse(update.message.from_user.username, update.message.text, settings["Identity"], settings["Temperature"]))