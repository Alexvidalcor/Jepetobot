# Importing libraries
import os
import pandas as pd
import pdfkit
from datetime import datetime


# Custom imports
from main import Update, ContextTypes, ReplyKeyboardMarkup, ReplyKeyboardRemove, ConversationHandler, InlineKeyboardButton, InlineKeyboardMarkup
from src.modules import logtool, db
from src.modules.security import security_user, security_file, security_crypto
from src.env.app_public_env import maxTokensCustomIdentity, dbPath, configBotResponses, dbName
from src.env.app_secrets_env import fileKey



settingSelected, buttonSelected, customSelected, customAnswer = range(4)

identityOptions = {

    "Kindly AI (default)":
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are kind",

    "Answer sarcastically":
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are very sarcastic",

    "Custom":
        "Custom"
}


@security_user.AdminFirewall
async def SettingsMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /settings is issued.

    username = update.message.from_user.username
    logtool.userLogger.info(f'{username} opened "settings"')

    replyKeyboard = [["Identity", "Temperature", "Costs", "Reset"]]

    await update.message.reply_text(
        "Settings section! "
        "Send /cancel to cancel.\n\n"
        "What do you want to configure?",
        reply_markup=ReplyKeyboardMarkup(
            replyKeyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Select your option",
            selective=True
        )
    )
    return settingSelected


@security_user.AdminFirewall
async def ValueAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        username = update.message.from_user.username
        context.chat_data["settingSelected"] = update.message.text

        logtool.userLogger.info(f'{username} chose {context.chat_data["settingSelected"]}')

        if context.chat_data["settingSelected"] == "Identity":

            settingOptions = [
                [InlineKeyboardButton(
                    list(identityOptions.keys())[0],
                    callback_data=list(identityOptions.keys())[0])],

                [InlineKeyboardButton(
                    list(identityOptions.keys())[1],
                    callback_data=list(identityOptions.keys())[1])],

                [InlineKeyboardButton(
                    list(identityOptions.keys())[2],
                    callback_data=list(identityOptions.keys())[2])],
            ]

        elif context.chat_data["settingSelected"] == "Temperature":
            settingOptions = [
                [
                    InlineKeyboardButton("0.1", callback_data=0.1),
                    InlineKeyboardButton("0.3", callback_data=0.3),
                    InlineKeyboardButton("0.5", callback_data=0.5),
                    InlineKeyboardButton("0.7", callback_data=0.7),
                    InlineKeyboardButton("0.9", callback_data=0.9),
                ]
            ]


        elif context.chat_data["settingSelected"] == "Costs":
            df = pd.read_sql_query(f'SELECT * FROM stats', db.con)

            df['cost_dollars'] = round(df['tokens_gpt']/1000 * 0.03 + df['tokens_dalle'] * 0.040 + df["tokens_whisper"] * 0.006 + df["tokens_tts"]/1000 * 0.015 + df["tokens_vision"] * 0.01105)

            '''
            NOTES:
            - Vision:
                The current bot is sending images with the following size: 1280x958
                The cost was adjusted with this info.
            '''

            # Get the current date
            currentDate = datetime.now()

            # Format the date
            formatDate = currentDate.strftime('%Y-%m-%d_%H:%M:%S')

            # Convert dataframe to html file
            htmlDfPath = f"src/temp/costs_{formatDate}.html"
            df.to_html(htmlDfPath, index=False)

            # Convert dataframe to pdf file. The reason is to avoid incompatibilities when viewing the csv file by third-party programs
            pdfDfPath = f"src/temp/costs_{formatDate}.pdf"
            pdfkit.from_file(htmlDfPath, pdfDfPath)   

            # Send option selected to user and remove keyboard selector
            await update.message.reply_text(
                "Costs selected", reply_markup=ReplyKeyboardRemove()
            )  

            # Send PDF file via Telegram bot
            with open(pdfDfPath, 'rb') as filePdf:
                await context.bot.send_document(chat_id=update.effective_chat.id, document=filePdf)

            # Generate new Fernet Key
            fernetFileKey = security_crypto.GenerateFernetKey(fileKey)

            # Encrypt and delete costs HTML file
            security_file.EncryptFile(htmlDfPath, fernetFileKey)
            os.remove(htmlDfPath)

            # Encrypt and delete costs PDF file
            security_file.EncryptFile(pdfDfPath, fernetFileKey)
            os.remove(pdfDfPath)

            logtool.userLogger.info(f'{username} sent a costs file')

            return ConversationHandler.END


        elif context.chat_data["settingSelected"] == "Reset":
            if os.path.exists(dbPath + "/" + dbName):
                os.remove(dbPath + "/" + dbName)
                db.TestDbConnection()
                
                # os.remove(f"{logsPath}/*.log")

                # EnableLogging()
                logtool.appLogger.info("------------Reseted")
                logtool.userLogger.warning("------------Reseted")
                logtool.errorsLogger.error("------------Reseted")

                await update.message.reply_text(
                    f"Conversations deleted successfully",
                    reply_markup=ReplyKeyboardRemove()
                )

            else:
                await update.message.reply_text(
                    f"Conversations not found",
                    reply_markup=ReplyKeyboardRemove()
                )
            return ConversationHandler.END

        await update.message.reply_text(
            f"Insert the new value to use in {context.chat_data['settingSelected']}",
            reply_markup=ReplyKeyboardRemove()
        )
        await update.message.reply_text("Please choose:",
                                        reply_markup=InlineKeyboardMarkup(
                                            settingOptions)
                                        )
        return buttonSelected
    except:
        await update.message.reply_text(
            "Canceled", reply_markup=ReplyKeyboardRemove()
        )
        logtool.userLogger.info(f'{username} canceled configuration')
        return ConversationHandler.END


async def Button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query
    await query.answer()

    user = query.from_user
    username = user.username
    logtool.userLogger.info(f'{username} chose {query.data}')

    await query.edit_message_text(text=f"Selected option: {query.data}")
    
    if context.chat_data["settingSelected"] == "Identity":
        context.chat_data["valueSelected"] = identityOptions[query.data]
    elif context.chat_data["settingSelected"] == "Temperature":
        context.chat_data["valueSelected"] = query.data

    configBotResponses[context.chat_data["settingSelected"]
             ] = context.chat_data["valueSelected"]

    if context.chat_data["valueSelected"] == "Custom":
        await update.callback_query.message.edit_text(
            "Insert new custom identity: "
        )
        return customAnswer
    else:
        logtool.userLogger.info(f'{username} finished configuration')
        return ConversationHandler.END


async def CustomAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    userCustomAnswer = update.message.text
    username = update.message.from_user.username

    if len(list(userCustomAnswer)) <= maxTokensCustomIdentity:
        await update.message.reply_text(
            f"Inserted the following identity: {userCustomAnswer}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            f"Your custom identity has {len(list(userCustomAnswer))}, the max is {maxTokensCustomIdentity}",
            reply_markup=ReplyKeyboardRemove()
        )

    context.chat_data["valueSelected"] = userCustomAnswer

    configBotResponses[context.chat_data["settingSelected"]
             ] = context.chat_data["valueSelected"]

    logtool.userLogger.info(f'{username} custom identity is: {userCustomAnswer}')
    logtool.userLogger.info(f'{username} finished configuration')
    return ConversationHandler.END
