
# Telegram libraries
from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

# Python libraries
import logging

# Custom importation
from src.modules.app_support import *
from src.requests import generate_response


# Log tool
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Initial vars needed
setting, identity, temperature = range(3)

# User logging decorator


def UsersFirewall(originalFunction):
    async def CheckPermissions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        if user["id"] in idUsersAllowed:
            return await originalFunction(update, context)
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!, you don't have permissions"
        )
    return CheckPermissions

@UsersFirewall
async def Start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /start is issued.
    user = update.effective_user

    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


@UsersFirewall
async def AiReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Reply the user message.
    await update.message.reply_text(generate_response(update.message.text))
    # user = update.message.from_user
    # print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))

@UsersFirewall
async def HelpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /help is issued.
    await update.message.reply_text("Help!")

@UsersFirewall
async def SettingsMenu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message when the command /settings is issued.
    user = update.message.from_user
    if user["id"] in idUsersAllowed:
        replyKeyboard = [["Identity", "Temperature"]]

        await update.message.reply_text(
            "Settings section! "
            "Send /cancel to cancel.\n\n"
            "What do you want to configure?",
            reply_markup=ReplyKeyboardMarkup(
                replyKeyboard,
                one_time_keyboard=True,
                input_field_placeholder="Identity or Temperature?"
            )
        )
        return setting

@UsersFirewall
async def ValueAnswer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settingSelected = update.message.text
    await update.message.reply_text(
        f"Insert the new value to use in {settingSelected}",
        reply_markup=ReplyKeyboardRemove(),
    )
    return

@UsersFirewall
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""

    user = update.message.from_user
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()

    )

    return ConversationHandler.END


def main() -> None:

    # Start the bot.
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegramToken).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", Start))
    application.add_handler(CommandHandler("help", HelpCommand))

    # Conversation handler to define custom settings
    convHandler = ConversationHandler(

        entry_points=[CommandHandler("settings", SettingsMenu)],

        states={
            setting: [MessageHandler(filters.TEXT, ValueAnswer)]
        },

        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(convHandler)

    # on non command i.e message - reply the message on Telegram
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, AiReply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
