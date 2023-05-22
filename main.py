
# Telegram libraries
from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, constants

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler,  InlineQueryHandler


# Custom importation
from src.modules.app_support import *
from src.modules.logging import *
from src.settings import *
from src.requests import AiReply, AiReplyInline
from src.permissions import UsersFirewall
from src.db import TestDbConnection


# Start Function
@UsersFirewall
async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /start is issued.
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Help function
@UsersFirewall
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
@UsersFirewall
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
    application.add_handler(InlineQueryHandler(AiReplyInline))

    # Conversation handler to define custom settings
    convHandler1 = ConversationHandler(

        entry_points=[CommandHandler("settings", SettingsMenu)],

        states={
            settingSelected: [MessageHandler(filters.TEXT, ValueAnswer)],
            buttonSelected: [CallbackQueryHandler(Button)],
            customAnswer: [MessageHandler(filters.TEXT, CustomAnswer)]
        },

        fallbacks=[CommandHandler("cancel", cancel)],
        per_chat=True,
        per_user=True
    )
    application.add_handler(convHandler1)

    # on non command i.e message - reply the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, AiReply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    TestDbConnection()
    main()
