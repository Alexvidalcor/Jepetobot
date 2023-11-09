
# Telegram libraries
from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, constants

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler,  InlineQueryHandler, CallbackContext


# Custom importation
from src.env.app_public_env import appVersion
from src.env.app_secrets_env import telegramToken
from src.modules import settings, responses, permissions, db



# Start Function
@permissions.UsersFirewall
async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /start is issued.
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Help function
@permissions.UsersFirewall
async def HelpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /help is issued.
    await update.message.reply_text(
        "---------------------------\n\n" \
        "<strong>Developer: </strong>Alexvidalcor\n\n" \
        "<strong>Source code: </strong><a href=\"https://github.com/Alexvidalcor/jepetobot\">Github Page\n\n</a>" \
        f"<strong>Version: </strong>{appVersion}\n\n" \
        "---------------------------",
    parse_mode=constants.ParseMode.HTML
)


# Cancel function
@permissions.UsersFirewall
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:

    # Start the bot.
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegramToken).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("start", Start))
    application.add_handler(CommandHandler("help", HelpCommand))
    application.add_handler(CommandHandler("cancel", cancel))

    # Inline query handler
    application.add_handler(InlineQueryHandler(responses.TextInputInline))

    # Conversation handler to define custom settings
    convHandler1 = ConversationHandler(

        entry_points=[CommandHandler("settings", settings.SettingsMenu)],

        states={
            settings.settingSelected: [MessageHandler(filters.TEXT, settings.ValueAnswer)],
            settings.buttonSelected: [CallbackQueryHandler(settings.Button)],
            settings.customAnswer: [MessageHandler(filters.TEXT, settings.CustomAnswer)]
        },

        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=True,
        per_user=True
    )
    application.add_handler(convHandler1)

    # on non command i.e VOICE message - reply the message on Telegram
    application.add_handler(MessageHandler(
        filters.VOICE & ~filters.COMMAND, responses.VoiceInput)) 

    # on non command i.e TEXT message - reply the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, responses.TextInput))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    db.TestDbConnection()
    main()
