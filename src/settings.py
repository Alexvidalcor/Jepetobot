from main import *
from src.permissions import UsersFirewall

settingSelected, buttonSelected, customSelected, customAnswer = range(4)


@UsersFirewall
async def SettingsMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /settings is issued.

    replyKeyboard = [["Identity", "Temperature"]]

    await update.message.reply_text(
        "Settings section! "
        "Send /cancel to cancel.\n\n"
        "What do you want to configure?",
        reply_markup=ReplyKeyboardMarkup(
            replyKeyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Identity or Temperature?",
            selective=True
        )
    )
    return settingSelected


@UsersFirewall
async def ValueAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        context.chat_data["settingSelected"] = update.message.text

        if context.chat_data["settingSelected"] == "Identity":

            identityOptions = [
                "You are Jepetobot, an artificial intelligence",
                "You are a very sarcastic human",
                "Custom"
            ]

            settingOptions = [
                [InlineKeyboardButton(
                    identityOptions[0],
                    callback_data=identityOptions[0])],

                [InlineKeyboardButton(
                    identityOptions[1],
                    callback_data=identityOptions[1])],

                [InlineKeyboardButton(
                    identityOptions[2],
                    callback_data=identityOptions[2])],
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
        await update.message.reply_text(
            f"Insert the new value to use in {context.chat_data['settingSelected']}",
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
