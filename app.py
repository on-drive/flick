import logging
from re import S

import constants
import cric_info

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram import Update, update

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


matches_list, matches_dict_list = cric_info.get_match_dict_list()


def start(update, context):
    username = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hello {username}, Welcome to my bot!"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Myself Crickinfo bot ,type /help to know my commands?",
    )


def help(update, context):
    update.message.reply_text(
        "Type /matches to fetch the list of all matches For a individual match type the index of the match from the matches list  after selecting any particular match Use /set <seconds> to set a timer"
    )


def match_detail(context: CallbackContext):
    job = context.job
    num = job.context
    # is_reply_numeric = update.message.text.isdigit()
    # is_reply_numeric = num.isdigit()

    # if is_reply_numeric:
    # match_number = int(update.message.text)
    match_number = int(num)
    # update.message.reply_text(
    # cric_info.get_match_details(
    #     matches_dict_list[match_number]["series_id"],
    #     matches_dict_list[match_number]["match_id"],
    # )
    # )
    text = cric_info.get_match_details(
        matches_dict_list[match_number]["series_id"],
        matches_dict_list[match_number]["match_id"],
    )
    context.bot.send_message(job.context, text=text)


# else:
#     # update.message.reply_text("Please enter a valid number. Thanks!")
#     text = "Please enter a valid number. Thanks!"
#     context.bot.send_message(job.context, text=text)


def matches(update, context):
    update.message.reply_text("Here's a list of current live matches:\n" + matches_list)


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    # try:
    # args[0] should contain the time for the timer in seconds
    due = int(context.args[0])
    if due < 0:
        update.message.reply_text("Sorry we can not go back to future!")
        return

    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(
        match_detail, due, context=chat_id, name=str(chat_id)
    )

    text = "Timer successfully set!"
    if job_removed:
        text += " Old one was removed."
    update.message.reply_text(text)

    # except (IndexError, ValueError):
    # update.message.reply_text("Usage: /set <seconds>")


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = (
        "Timer successfully cancelled!" if job_removed else "You have no active timer."
    )
    update.message.reply_text(text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(constants.API_KEY, use_context=True)

    dp = updater.dispatcher

    # command handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("matches", matches))
    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("unset", unset))

    # message handler
    # dp.add_handler(MessageHandler(Filters.text, match_detail))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
