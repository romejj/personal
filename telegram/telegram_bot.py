from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
import logging

updater = Updater(token='674969923:AAHd5L-jrWsDFKDn1NZp49dt1J4FeO2-z8k', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Add event handler that returns start() function when user inputs /start in chat
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Love you cutie!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Add an event handler that listens for messages and echos them
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# Start the bot
updater.start_polling()

