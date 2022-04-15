"""
    Main code for the Bible-bot with Telegram
"""
import logging as log
from time import sleep
from typing import Any

import telebot
import telebot.types as types

from utils import constants
from telegram_pages import pages

bot = telebot.TeleBot(constants.TOKEN)
tg_pages = pages.TelegramPages()

########################################################################
################          KEYBOARD FUNCTIONS         ###################
########################################################################
def show_mainkeyboard(chat_message: Any):
    """Show the main keyboard

    Args:
        chat_message (Any):
            On what chat the keyboard will be shown.
    """
    start_markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=False
    )
    for item in list(constants.COMMANDS.keys()):
        start_markup.row(f"/{item}")
    start_markup.row("/hide_keyboard")
    bot.send_message(
        chat_message.from_user.id, "⌨️❔", reply_markup=start_markup
    )


@bot.message_handler(commands=["hide_keyboard"])
def command_hide(chat_message: Any):
    """Hide the keyboard

    Args:
        chat_message (Any):
            On what chat the keyboard will be hidden.
    """
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_message.chat.id, "⌨💤...", reply_markup=hide_markup)


########################################################################
################            BOT INTERACTION          ###################
########################################################################
@bot.message_handler(commands=["start"])
def command_start(chat_message: Any):
    """Start the conversation of the bot

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    user_id = chat_message.chat.id
    name = chat_message.chat.first_name
    message = tg_pages.start(user_id, name)
    bot.send_message(user_id, message)
    command_help(chat_message)


@bot.message_handler(commands=["send_chapter"])
def command_send_chapter(chat_message: Any):
    """Send chapter bot interaction

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    user_id = chat_message.chat.id
    message = tg_pages.send_chapter(user_id)
    for single_message in message:
        bot.send_message(user_id, single_message)
    show_mainkeyboard(chat_message)


@bot.message_handler(commands=["verse"])
def command_verse(chat_message: Any):
    """Set verse

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.verse(user_id)
    for single_message in message:
        bot.send_message(user_id, single_message)


@bot.message_handler(commands=["information"])
def command_information(chat_message: Any):
    """Show information

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.information(user_id)
    bot.send_message(user_id, message)
    show_mainkeyboard(chat_message)


@bot.message_handler(commands=["help"])
def command_help(chat_message: Any):
    """Show help message

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.help(user_id)
    bot.send_message(user_id, message)
    show_mainkeyboard(chat_message)


@bot.message_handler(commands=["language"])
def command_language(chat_message):
    """Modify language initial message and state

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.language(user_id)
    bot.send_message(user_id, message)


@bot.message_handler(commands=["choose_book"])
def command_book(chat_message):
    """Modify book initial message and state

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.book(user_id)
    bot.send_message(user_id, message)


@bot.message_handler(commands=["choose_chapter"])
def command_chapter(chat_message):
    """Modify book chapter message and state

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message = tg_pages.chapter(user_id)
    bot.send_message(user_id, message)


@bot.message_handler(commands=["bible_version"])
def command_bible_version(chat_message):
    """Modify bible version initial message and state

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    command_hide(chat_message)
    user_id = chat_message.chat.id
    message, versions = tg_pages.bible_version(user_id)

    if versions != []:
        version_markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=False
        )
        for each in range(len(versions)):
            version_markup.row(versions[each])
        bot.send_message(
            chat_message.from_user.id, "⌨️", reply_markup=version_markup
        )
    else:
        bot.send_message(user_id, message)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def command_default(chat_message):
    """Main interaction menu for income

    Args:
        chat_message (Any):
            On what chat the bot will interact.
    """
    user_id = chat_message.chat.id
    message = tg_pages.default(user_id, chat_message.text)
    message = [message] if type(message) == str else message
    for single_message in message:
        bot.send_message(user_id, single_message)
    show_mainkeyboard(chat_message)


########################################################################
################            MAIN FUNCTION             ##################
########################################################################
if __name__ == "__main__":
    while True:
        try:
            log.info("Starting bot")
            bot.polling(none_stop=True, timeout=30)
        except Exception as err:
            log.error("Bot polling error: {0}".format(err.args))
            bot.stop_polling()
            sleep(60)
