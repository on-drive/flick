import logging

import constant
import cric_info

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


a, b = cric_info.get_match_list()


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi!")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text + "\nbaba op")


def match_detail(update, context):

    is_reply_numeric = update.message.text.isdigit()

    if is_reply_numeric:
        match_number = int(update.message.text)
        update.message.reply_text(
            cric_info.get_match_details(
                b[match_number]["series_id"],
                b[match_number]["match_id"],
            )
        )
    else:
        update.message.reply_text("Please enter a valid number. Thanks!")


def matches(update, context):
    update.message.reply_text("Here's a list of current live matches:\n" + a)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    updater = Updater(constant.DOGE_BOT_API_KEY, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("matches", matches))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, match_detail))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
