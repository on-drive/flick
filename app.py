import logging

import constants
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
        text=constants.info_text,
    )


def help(update, context):
    reply = constants.help_text
    update.message.reply_text(reply)


x = 2


def match_detail(context: CallbackContext) -> None:
    job = context.job
    context.bot.send_message(
        job.context,
        text=cric_info.get_match_details(
            matches_dict_list[x]["series_id"],
            matches_dict_list[x]["match_id"],
        ),
    )


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def set_timer_once(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        global x
        x = int(context.args[0])
        if x < 0:
            update.message.reply_text(constants.negative_match)
            return
        context.job_queue.run_once(
            match_detail, when=0, context=chat_id, name=str(chat_id)
        )
    except (IndexError, ValueError):
        update.message.reply_text(constants.except_reply2)


def set_timer(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(constants.negative_time)
            return
        global x
        x = int(context.args[1])
        if x < 0:
            update.message.reply_text(constants.negative_match)
            return
        context.job_queue.run_once(
            match_detail, when=0, context=chat_id, name=str(chat_id)
        )
        context.job_queue.run_repeating(
            match_detail, due, context=chat_id, name=str(chat_id)
        )

        text = constants.timer_success
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text(constants.except_reply)


def matches(update, context):
    update.message.reply_text(constants.live_matches + matches_list)


def unset(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = constants.timer_cancel if job_removed else constants.no_timer
    update.message.reply_text(text)


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = constants.default_text

    update.message.reply_text(response)


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
    dp.add_handler(CommandHandler("setonce", set_timer_once))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
