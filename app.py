import logging

import constant
import cric_info


from telegram import Update


from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)


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
    # chat_id = update.message.chat_id
    # try:
    # args[0] should contain the time for the timer in seconds
    # match_number = int(context.args[0])
    # if match_number < 0:
    #     update.message.reply_text("Enter a valid match number ")
    #     return
    # due = int(context.args[1])
    # if due < 0:
    #     update.message.reply_text("Sorry we can not go back to future!")
    #     return

    # context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id))

    text = cric_info.get_match_details(
        matches_dict_list[0]["series_id"],
        matches_dict_list[0]["match_id"],
    )
    # if job_removed:
    #     text += ' Old one was removed.'
    # update.message.reply_text(text)
    print(text)

    # except (IndexError, ValueError):
    #     update.message.reply_text("Usage: fald onds>")

    # is_reply_numeric = update.message.text.isdigit()

    # if is_reply_numeric:
    #     match_number = int(update.message.text)
    #     update.message.reply_text(
    #         cric_info.get_match_details(
    #             matches_dict_list[match_number]["series_id"],
    #             matches_dict_list[match_number]["match_id"],
    #         )
    #     )
    # else:
    #     update.message.reply_text("Please enter a valid number. Thanks!")


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(
        job.context,
        text=cric_info.get_match_details(
            matches_dict_list[0]["series_id"],
            matches_dict_list[0]["match_id"],
        ),
    )


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    # try:
    # args[0] should contain the time for the timer in seconds
    due = int(context.args[0])
    if due < 0:
        update.message.reply_text("Sorry we can not go back to future!")
        return

    context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id))

    text = "Timer successfully set!"
    update.message.reply_text(text)

    # except (IndexError, ValueError):
    #     update.message.reply_text("Usage: /set <seconds>")


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
    dp.add_handler(CommandHandler("match", match_detail))
    dp.add_handler(CommandHandler("repeat", set_timer))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, start))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
