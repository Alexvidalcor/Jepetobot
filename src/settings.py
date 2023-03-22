import os

from main import *
from src.permissions import UsersFirewall

settingSelected, buttonSelected, customSelected, customAnswer = range(4)

identityOptions = {

    "Kindly AI (default)":
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are kind",

    "Answer sarcastically":
        "You play jepetobot and you just have to respond as if you were that character. You are a member of a chat that talks about many topics and you can have opinions on those topics. Your purpose in that chat is to answer the questions in the most human way possible. Your answers are very sarcastic",

    "Custom":
        "Custom"
}


@UsersFirewall
async def SettingsMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /settings is issued.

    replyKeyboard = [["Identity", "Temperature", "Reset"]]

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


@UsersFirewall
async def ValueAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.chat_data["settingSelected"] = update.message.text

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

        elif context.chat_data["settingSelected"] == "Reset":
            if os.path.exists(dbPath):
                os.remove(dbPath)
                TestDbConnection()
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
        return ConversationHandler.END


async def Button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""

    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
    
    if context.chat_data["settingSelected"] == "Identity":
        context.chat_data["valueSelected"] = identityOptions[query.data]
    elif context.chat_data["settingSelected"] == "Temperature":
        context.chat_data["valueSelected"] = query.data

    settings[context.chat_data["settingSelected"]
             ] = context.chat_data["valueSelected"]

    if context.chat_data["valueSelected"] == "Custom":
        await update.callback_query.message.edit_text(
            "Insert new custom identity: "
        )
        return customAnswer
    else:
        return ConversationHandler.END


async def CustomAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    userCustomAnswer = update.message.text

    await update.message.reply_text(
        f"Inserted the following identity: {userCustomAnswer}",
        reply_markup=ReplyKeyboardRemove()
    )

    context.chat_data["valueSelected"] = userCustomAnswer

    settings[context.chat_data["settingSelected"]
             ] = context.chat_data["valueSelected"]

    return ConversationHandler.END
