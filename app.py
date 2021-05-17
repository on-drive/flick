import logging

import constant
import cric_info

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


matches_list, matches_dict_list = cric_info.get_match_dict_list()


def start(update, context):
    update.message.reply_text("Hi!")


def help(update, context):
    update.message.reply_text("Help!")


def match_detail(update, context):

    is_reply_numeric = update.message.text.isdigit()

    if is_reply_numeric:
        match_number = int(update.message.text)
        update.message.reply_text(
            cric_info.get_match_details(
                matches_dict_list[match_number]["series_id"],
                matches_dict_list[match_number]["match_id"],
            )
        )
    else:
        update.message.reply_text("Please enter a valid number. Thanks!")


def matches(update, context):
    update.message.reply_text("Here's a list of current live matches:\n" + matches_list)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(constant.DOGE_BOT_API_KEY, use_context=True)

    dp = updater.dispatcher

    # command handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("matches", matches))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, match_detail))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
