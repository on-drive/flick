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
    username = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hello {username}, Welcome to my bot!"
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Myself Crickinfo bot ,type /help to know my commands?",
    )


def help(update, context):
    reply = """/matches - Show's the list of current matches along with indexe's which can be used by set command
/set - Takes in 2 argument first is the timeinterval(in sec) and second is the match index ex- /set 5 0
/unset - Cancel's the timer and no more data will be fetched
            
            """
    update.message.reply_text(reply)


# def match_detail(update, context):
#     # chat_id = update.message.chat_id
#     # try:
#     # args[0] should contain the time for the timer in seconds
#     # match_number = int(context.args[0])
#     # if match_number < 0:
#     #     update.message.reply_text("Enter a valid match number ")
#     #     return
#     # due = int(context.args[1])
#     # if due < 0:
#     #     update.message.reply_text("Sorry we can not go back to future!")
#     #     return

#     # context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id))

#     text = cric_info.get_match_details(
#         matches_dict_list[0]["series_id"],
#         matches_dict_list[0]["match_id"],
#     )
#     # if job_removed:
#     #     text += ' Old one was removed.'
#     # update.message.reply_text(text)
#     print(text)

#     # except (IndexError, ValueError):
#     #     update.message.reply_text("Usage: fald onds>")

#     # is_reply_numeric = update.message.text.isdigit()

#     # if is_reply_numeric:
#     #     match_number = int(update.message.text)
#     #     update.message.reply_text(
#     #         cric_info.get_match_details(
#     #             matches_dict_list[match_number]["series_id"],
#     #             matches_dict_list[match_number]["match_id"],
#     #         )
#     #     )
#     # else:
#     #     update.message.reply_text("Please enter a valid number. Thanks!")


x = 2


def alarm(context: CallbackContext) -> None:
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(
        job.context,
        text=cric_info.get_match_details(
            matches_dict_list[x]["series_id"],
            matches_dict_list[x]["match_id"],
        ),
    )


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
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("Sorry we can not go back to future!")
            return
        global x
        x = int(context.args[1])
        if x < 0:
            update.message.reply_text("Enter a valid match number ")
            return

        context.job_queue.run_repeating(alarm, due, context=chat_id, name=str(chat_id))

        text = "Timer successfully set!"
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text("Usage: /set <seconds>")


def matches(update, context):
    update.message.reply_text("Here's a list of current live matches:\n" + matches_list)


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = (
        "Timer successfully cancelled!" if job_removed else "You have no active timer."
    )
    update.message.reply_text(text)


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = "Sorry we don't entertain this command, Type /help to know my command's"

    update.message.reply_text(response)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(constant.API_KEY, use_context=True)

    dp = updater.dispatcher

    # command handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("matches", matches))
    # dp.add_handler(CommandHandler("match", match_detail))
    dp.add_handler(CommandHandler("set", set_timer))
    dp.add_handler(CommandHandler("unset", unset))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
