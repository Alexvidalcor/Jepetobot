# Python libraries
import openai
import urllib.request

# Custom modules
from main import *
from src.modules import permissions, db, stats, logtool
from src.env.app_support import openaiToken, configBotResponses
from src.env.app_public_env import maxTokensResponse

# Get OpenAI token
openai.api_key = openaiToken


def FormatCompletionMessages(cur, username, chatid, identity, promptUser, option="prerequest"):

    logtool.userLogger.info(f'{username} sent a message')

    results = db.GetUserMessagesToReply(username, chatid)
    resultsFormatted = eval(str(results).replace("None", "'None'"))

    conversationFormatted = [{"role": "system", "content": identity}]
    for row in resultsFormatted:
        conversationFormatted.append({"role": "user", "content": row[2]})
        conversationFormatted.append({"role": "assistant", "content": row[6]})

    if option == "prerequest":
        conversationFormatted.pop()

    return conversationFormatted


def GenerateResponse(username, prompt, chatid, identity, temp):
    # Import latest connection object
    from src.modules.db import con, cur

    db.InsertUserMessage(username, prompt, chatid)
    messagesFormatted = FormatCompletionMessages(
        cur, username, chatid, identity, prompt)

    completions = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=messagesFormatted,
        max_tokens=maxTokensResponse,
        n=1,
        stop=None,
        temperature=float(temp),
    )

    answerProvided = completions["choices"][0]["message"]["content"]

    db.InsertAssistantMessage(username, answerProvided, chatid)

    messagesFormattedPost = FormatCompletionMessages(
        cur, username, chatid, identity, prompt, option="postrequest")

    stats.StatsNumTokens(username, messagesFormattedPost)
    logtool.userLogger.info('Jepetobot replied a message')

    return answerProvided


def GenerateImage(promptUser):
    try:
        responseImage = openai.Image.create(
            prompt=promptUser,
            n=1,
            size="256x256"
        )

        return responseImage['data'][0]['url']
    
    except openai.error.InvalidRequestError:
        return "https://openclipart.org/image/2400px/svg_to_png/167093/StopSign-nofont.png"

    
@permissions.UsersFirewall
async def AiReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.text.startswith("IMAGE:"):
    #Reply a dalle image
        await update.message.reply_photo(GenerateImage(update.message.text.replace("IMAGE:","")))

    else:
    # Reply the user message.
        await update.message.reply_text(GenerateResponse(update.message.from_user.username, update.message.text, update.message.chat_id, configBotResponses["Identity"], configBotResponses["Temperature"]))


@permissions.UsersFirewall
async def AiReplyInline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Handle the inline query. This is run when you type: @botusername <query>"""

    query = update.inline_query.query

    if query == "":
        return

    results = [

        InlineQueryResultArticle(
            id="1",
            title="ReplyInline",
            description="Click here to get an answer",
            thumbnail_url="https://raw.githubusercontent.com/Alexvidalcor/jepetobot/master/src/images/Readme-logo2.jpg",
            input_message_content=InputTextMessageContent(query)
        )
    ]

    await update.inline_query.answer(results)
