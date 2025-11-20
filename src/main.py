"""
    Main code for the Bible-bot with Telegram
"""
import logging as log
import logging.handlers
import signal
import sys
from time import sleep
from typing import Any

import telebot
import telebot.types as types

from utils import constants
from telegram_pages import pages

# Configure logging with rotation to prevent SD card fill-up
log_formatter = log.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# File handler with rotation (max 5MB per file, keep 3 backups)
file_handler = logging.handlers.RotatingFileHandler(
    'bible_bot.log',
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(log.INFO)

# Console handler
console_handler = log.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(log.INFO)

# Configure root logger
log.basicConfig(
    level=log.INFO,
    handlers=[file_handler, console_handler]
)

bot = telebot.TeleBot(constants.TOKEN)
tg_pages = pages.TelegramPages()

# Graceful shutdown handler
shutdown_requested = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global shutdown_requested
    log.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_requested = True
    try:
        bot.stop_polling()
    except Exception as e:
        log.error(f"Error during shutdown: {e}")

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

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
    log.info("Bible Telegram Bot starting...")
    log.info(f"Bot token configured: {constants.TOKEN is not None}")
    
    retry_count = 0
    max_retries = 5
    
    while not shutdown_requested:
        try:
            log.info(f"Starting bot polling (attempt {retry_count + 1})")
            bot.polling(none_stop=True, timeout=30)
            retry_count = 0  # Reset on successful run
        except KeyboardInterrupt:
            log.info("Bot stopped by user")
            break
        except Exception as err:
            retry_count += 1
            log.error(f"Bot polling error (attempt {retry_count}/{max_retries}): {err}")
            bot.stop_polling()
            
            if retry_count >= max_retries:
                log.critical(f"Max retries ({max_retries}) reached. Exiting.")
                sys.exit(1)
            
            sleep_time = min(60 * retry_count, 300)  # Max 5 minutes
            log.info(f"Retrying in {sleep_time} seconds...")
            sleep(sleep_time)
    
    log.info("Bible Telegram Bot stopped gracefully")
