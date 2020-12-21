from telegram.ext import Updater, CommandHandler
import logging

from src.config.auth import token
from src.requests import GetSubs

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):    
    logger.info('He recibido un comando start')
    context.bot.send_message(chat_id=update.effective_chat.id,text=GetSubs())

if __name__ == '__main__':

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()



