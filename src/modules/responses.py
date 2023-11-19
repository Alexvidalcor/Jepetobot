# Python libraries
import openai
import urllib.request
import os
import datetime
import base64
from cryptography.fernet import Fernet

# Custom modules
from main import *
from src.modules import security, db, stats, logtool
from src.env.app_secrets_env import openaiToken, fileKey
from src.env.app_public_env import maxTokensResponse, configBotResponses, voiceChoice

# Get OpenAI token
openai.api_key = openaiToken


def GetCurrentDatetime():
    datetimeCheck = datetime.datetime.now()
    formattedDatetime = datetimeCheck.strftime("%Y-%m-%d %H:%M:%S")
    return formattedDatetime


def FormatCompletionMessages(cur, username, chatid, identity, promptUser, option="prerequest"):

    logtool.userLogger.info(f'{username} sent a message')

    results = db.GetUserMessagesToReply(username, chatid)
    resultsFormatted = eval(str(results).replace("None", "'None'"))

    conversationFormatted = [{"role": "system", "content": identity}]
    for row in resultsFormatted:
        conversationFormatted.append({"role": "user", "content": row[2]})
        conversationFormatted.append({"role": "assistant", "content": row[8]})

    if option == "prerequest":
        conversationFormatted.pop()

    return conversationFormatted


def GenerateTextReply(username, prompt, chatid, identity, temp, via):
    # Import latest connection object
    from src.modules.db import con, cur

    currentDateTime = GetCurrentDatetime()

    db.InsertUserMessage(username, prompt, chatid, via, currentDateTime)
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

    db.InsertAssistantMessage(username, answerProvided, chatid , via, currentDateTime)

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
        return "src/images/App-image1.png"


def SpeechToText(userVoicePath):
    audioFile= open(userVoicePath, "rb")
    transcript = openai.audio.transcriptions.create(
    model="whisper-1", 
    file=audioFile
    )
    return transcript


def TextToSpeech(userVoiceNoteTranscripted, botVoicePath, voiceChoice):
    response = openai.audio.speech.create(
    model="tts-1",
    voice=voiceChoice,
    input=userVoiceNoteTranscripted,
    )

    response.stream_to_file(botVoicePath)


def AudioTranscriptProcessor(userVoiceNoteTranscripted):
    if userVoiceNoteTranscripted.lower().startswith("image") or userVoiceNoteTranscripted.lower().startswith("y mage"):
        result = ["image", GenerateImageReply(userVoiceNoteTranscripted[5::])]
    else:
        result = ["text", False]
    
    return result


@security.UsersFirewall
async def VoiceInput(update: Update, context: CallbackContext) -> None:

    # Get current datetime for database tasks
    currentDateTime = GetCurrentDatetime()

    # Get basic info about the voice note file and prepare it for downloading
    userVoiceNoteId = await context.bot.get_file(update.message.voice.file_id)

    userVoicePath = f"src/temp/user_voice_note-{update.message.from_user.username}-{update.message.chat_id}.mp3"

    # Download the voice note as a file
    await userVoiceNoteId.download_to_drive(userVoicePath)

    # Transcript voice note file to text
    audioTranscript = SpeechToText(userVoicePath)

    # Generate new Fernet Key
    fernetFileKey = security.GenerateFernetKey()

    # Encrypt user voice note
    security.EncryptFile(userVoicePath, fernetFileKey)

    # Remove user voice note
    os.remove(userVoicePath)

    # Process the previous transcription to check if a specific voice command was pronounced
    transcriptProcessed = AudioTranscriptProcessor(audioTranscript.text)

    # Performs different actions if a specific voice command was detected
    if transcriptProcessed[0] == "text":

        botAudioReply = GenerateTextReply(update.message.from_user.username, audioTranscript.text, update.message.chat_id, configBotResponses["Identity"], configBotResponses["Temperature"], "voice")

        botVoicePath = f"src/temp/bot_voice_note-{update.message.from_user.username}-{update.message.chat_id}.mp3"

        botVoiceNoteGeneration = TextToSpeech(botAudioReply, botVoicePath, voiceChoice)

        await update.message.reply_voice(botVoicePath)

        # Encrypt bot voice note
        security.EncryptFile(botVoicePath, fernetFileKey)
        
        # Remove bot voice note
        os.remove(botVoicePath)
    
    elif transcriptProcessed[0] == "image":
        await update.message.reply_photo(GenerateImageReply(audioTranscript.text[5::]))



@security.UsersFirewall
async def TextInput(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message.text.startswith("IMAGE:"):
    #Reply a dalle image
        await update.message.reply_photo(GenerateImageReply(update.message.text.replace("IMAGE:","")))

    else:
    # Reply the user message.
        await update.message.reply_text(GenerateTextReply(update.message.from_user.username, update.message.text, update.message.chat_id, configBotResponses["Identity"], configBotResponses["Temperature"], "text"))


@security.UsersFirewall
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
