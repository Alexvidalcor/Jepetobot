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


def GenerateTextReply(username, prompt, chatid, identity, temp):
    # Import latest connection object
    from src.modules.db import con, cur

    db.InsertUserMessage(username, prompt, chatid)
    messagesFormatted = FormatCompletionMessages(
        cur, username, chatid, identity, prompt)

    completions = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messagesFormatted,
        max_tokens=maxTokensResponse,
        n=1,
        stop=None,
        temperature=float(temp)
    )

    answerProvided = completions.choices[0].message.content

    db.InsertAssistantMessage(username, answerProvided, chatid)

    messagesFormattedPost = FormatCompletionMessages(
        cur, username, chatid, identity, prompt, option="postrequest")

    stats.StatsNumTokens(username, messagesFormattedPost)
    logtool.userLogger.info('Jepetobot replied a message')

    return answerProvided


def GenerateImageReply(promptUser):
    try:
        responseImage = openai.images.generate(
            model="dall-e-3",
            prompt=promptUser,
            n=1,
            size="1024x1024",
            quality="standard"
        )
        return responseImage.data[0].url
    
    except openai.BadRequestError:
        return "https://openclipart.org/image/2400px/svg_to_png/167093/StopSign-nofont.png"



def SpeechToText():
    audioFile= open("src/temp/user_voice_note.mp3", "rb")
    transcript = openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audioFile
    )
    return transcript


def TextToSpeech(userVoiceNoteTranscripted):
    response = openai.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=userVoiceNoteTranscripted,
    )

    response.stream_to_file("src/temp/bot_voice_note.mp3")


def AudioTranscriptProcessor(userVoiceNoteTranscripted):
    if userVoiceNoteTranscripted.lower().startswith("image") or userVoiceNoteTranscripted.lower().startswith("y mage"):
        result = ["image", GenerateImageReply(userVoiceNoteTranscripted[5::])]
    else:
        result = ["text", False]
    
    return result


@permissions.UsersFirewall
async def VoiceInput(update: Update, context: CallbackContext) -> None:

    # get basic info about the voice note file and prepare it for downloading
    new_file = await context.bot.get_file(update.message.voice.file_id)

    # download the voice note as a file
    await new_file.download_to_drive("src/temp/user_voice_note.mp3")

    audioTranscript = SpeechToText()
    transcriptProcessed = AudioTranscriptProcessor(audioTranscript.text)

    if transcriptProcessed[0] == "text":

        botAudioReply = GenerateTextReply(update.message.from_user.username, audioTranscript.text, update.message.chat_id, configBotResponses["Identity"], configBotResponses["Temperature"])
        botVoiceNoteGeneration= TextToSpeech(botAudioReply)
        await update.message.reply_voice("src/temp/bot_voice_note.mp3")
    
    elif transcriptProcessed[0] == "image":
        await update.message.reply_photo(GenerateImageReply(audioTranscript.text[5::]))


@permissions.UsersFirewall
async def TextInput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.text.startswith("IMAGE:"):
    #Reply a dalle image
        await update.message.reply_photo(GenerateImageReply(update.message.text.replace("IMAGE:","")))

    else:
    # Reply the user message.
        await update.message.reply_text(GenerateTextReply(update.message.from_user.username, update.message.text, update.message.chat_id, configBotResponses["Identity"], configBotResponses["Temperature"]))


@permissions.UsersFirewall
async def TextInputInline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

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
