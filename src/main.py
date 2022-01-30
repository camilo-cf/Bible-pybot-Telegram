"""
MIT License
Copyright (c) 2020 Camilo A. Cáceres
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import Bible
import Database_control

import logging
import telebot
from telebot import types
import numpy as np
from googletrans import Translator
import time
import logging as log
import os


########################################################################
######################         Constants          ###################### 
########################################################################

# Telegram TOKEN
TOKEN = os.getenv("BOT_TOKEN")

#create a new Telegram Bot object
bot = telebot.TeleBot(TOKEN)

# command description used in the "help" command
commands = {  
    'start'             : '☝ Know what can I do',
    'send_chapter'      : '📧 Send now the chapter to read',
    'verse'             : '⛪ Request a Bible passage',
    'information'       : '📒 Know your information and settings for this bot',
    'help'              : '❔ Gives you information about the available commands',
    'subscribe'          : '📚 Receive 1 Bible chapter every day at a given time or Cancel it',
    'language'          : '🌎 Select your preferred language',
    'choose_book'       : '📖 Select the current bible book you are reading',
    'choose_chapter'    : '📑 Select the current chapter you want to start reading',
    'bible_version'     : '📕 Select the bible version'
}


########################################################################
######################         LANGUAGES          ###################### 
########################################################################

# Translator constructor
translator = Translator()

# Available Languages and Versions in the API
f = open("languages_api.txt", "r")
bible_api_list = []
for x in f:
    bible_api_list.append(x[4:])

dict_api_version={}
languages_api=[]

for each_language in bible_api_list:
    language = each_language.split(":")[0]
    languages_api.append(language)
    dict_api_version[language]=[]

acronyms_api=[]
version_api=[]

for each in bible_api_list:
    language = each.split(":")[0]
    acronym= each.split("(")[-1].split(")")[0]
    version= each.split(":")[1].split(acronym)[0][:-1]
    
    acronyms_api.append(acronym)
    version_api.append(version)

    dict_api_version[language].append(version)

dict_api_ver2acr = dict(zip(version_api, acronyms_api))
dict_api_acr2ver = dict(zip(acronyms_api, version_api))
unique_languages_api = set(languages_api)

# Available translation languages
f = open("language_translate.txt", "r")
languages_translation = []
for each in f:
    languages_translation.append(each.split("\n")[0])

# Languages comparison
languages_translation_set = set(languages_translation)
lang_ver_transl = languages_translation_set.intersection(unique_languages_api)
lang_transl = languages_translation_set.difference(unique_languages_api)


########################################################################
################         SUPPORT FUNCTIONS           ###################
########################################################################

def verify_language(language_input, lang_ver_transl=list(lang_ver_transl), lang_transl=list(lang_transl)):
    '''

    '''
    similarity_vec=[]
    languages = lang_transl + lang_ver_transl
    language_input = translator.translate(language_input, dest='english').text
    for each in languages:
        similarity_vec.append(Bible.similar(language_input,each))

    return languages[np.argmax(similarity_vec)]


def verify_version(version_input, versions=list(dict_api_ver2acr.keys())):
    '''
    '''
    similarity_vec=[]
    
    for each in versions:
        similarity_vec.append(Bible.similar(version_input,each))

    return versions[np.argmax(similarity_vec)]

def send_translated_message(id, text, language="English"):
    '''
    '''
    try:
        if language == "English":
            bot.send_message(id, text)
        else:
            text = Bible.translate_message(text, language=language, src="English")
            text = text.replace("/ ","/")
            bot.send_message(id, text)
    except (Exception) as exception:
        logging.critical("In send translated message - Exception: ", exception)
        print("Connection Error")
        # DO NOT try to send the daily verse or any service if the user blocked the bot
        #send_translated_message(id, text, language)
        

########################################################################
################         ACTION FUNCTIONS           ###################
########################################################################

# start page
@bot.message_handler(commands=['start'])
def command_start(m):
    id = m.chat.id
    name = m.chat.first_name

    connection, cursor = Database_control.create_db()
    verify_id = Database_control.verify_id(cursor, id)    
    if verify_id == False:
        Database_control.add_user(connection, cursor, id, name)
    language = Database_control.get_language(cursor, id)
    Database_control.close_db(connection)

    start_text="☝ This bot is a free service for educational purposes \nThis bot 🤖 can: \n\t1. Send you daily 1 chapter of the Bible in a sequence ('/subscribe') \n\t2. If you are not subscribed or want to advance more, you can manually request the chapter ('/send_chapter'). \n\t3.❓ Also you can ask for any verse or passage ('/verse') \n\nGo to help ('/help') for more information"
    send_translated_message(m.chat.id, start_text, language)  # Send start text
    show_mainkeyboard(m)


# send_chapter page
@bot.message_handler(commands=['send_chapter'])
def command_send_chapter(m):

    id = m.chat.id     
    connection, cursor = Database_control.create_db()   
    book = Database_control.get_book(cursor, id)
    origin_language = Database_control.get_language(cursor, id)
    chapter = Database_control.get_chapter(cursor, id)
    bible_version = Database_control.get_bible_version(cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)

    
    if verify_id:
        send_translated_message(id, "Sending chapter  ...", language) 
        
        message = " ".join([book, str(chapter)]) 
            
        try:
            if origin_language in lang_ver_transl:
                n_message = message
                response = Bible.get_message(n_message, bible_version)
            else:
                n_message = Bible.translate_message(message, language="English", src=origin_language)
                response = Bible.get_message(n_message, bible_version)
                response = Bible.translate_message(response, origin_language)
        except (Exception) as exception:
            response = "Error - please retry"
            logging.critical("In send chapter page - Exception: ", exception)
        
        send_translated_message(id, n_message, language)
        response = [i for i in telebot.util.split_string(response, 3000)]
        for each_message in response:
            send_translated_message(id,each_message, language)

        next_chapter = Bible.get_next_chapter(message)
        next_book = next_chapter.split(" ")[0]
        next_chapter = next_chapter.split(" ")[1]

        Database_control.set_book(connection, cursor, next_book, id)
        Database_control.set_chapter(connection, cursor, next_chapter, id)
        
        Database_control.set_mod_default(connection, cursor, id)
        Database_control.close_db(connection)
        show_mainkeyboard(m)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        Database_control.close_db(connection)
        command_start(m)

def command_send_chapter_crontab(id):
    
    connection, cursor = Database_control.create_db()   
    book = Database_control.get_book(cursor, id)
    origin_language = Database_control.get_language(cursor, id)
    chapter = Database_control.get_chapter(cursor, id)
    bible_version = Database_control.get_bible_version(cursor, id)
    language = Database_control.get_language(cursor, id)

    send_translated_message(id, "Sending daily chapter", language) 
    
    message = " ".join([book, str(chapter)]) 
        
    try:
        if origin_language in lang_ver_transl:
            n_message = message
            response = Bible.get_message(n_message, bible_version)
        else:
            n_message = Bible.translate_message(message, language="English", src=origin_language)
            response = Bible.get_message(n_message, bible_version)
            response = Bible.translate_message(response, origin_language)

    except (Exception) as exception:
            response = "Error - please retry"
            logging.critical("In send command_send_chapter_crontab - Exception: ", exception)

    response = [i for i in telebot.util.split_string(response, 3000)]
    
    send_translated_message(id, n_message, language)
    
    for each_message in response:
        send_translated_message(id,each_message, language)

    next_chapter = Bible.get_next_chapter(message)
    next_book = next_chapter.split(" ")[0]
    next_chapter = next_chapter.split(" ")[1]

    Database_control.set_book(connection, cursor, next_book, id)
    Database_control.set_chapter(connection, cursor, next_chapter, id)
    
    Database_control.set_mod_default(connection, cursor, id)
    Database_control.close_db(connection)


# set verse page
@bot.message_handler(commands=['verse'])
def command_verse(m):
    
    command_hide(m)
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
    Database_control.set_verse(connection, cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        send_translated_message(id, "Type the desired passage", language)
        Example = "Examples: \nJohn 14:6 \nGenesis 2:1-4 \nLuke 3"
        send_translated_message(id, Example, language)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        command_start(m)

        
    
# information page
@bot.message_handler(commands=['information'])
def command_information(m):
    id = m.chat.id
       
    connection, cursor = Database_control.create_db()
    status = Database_control.get_status(cursor, id)
    language = Database_control.get_language(cursor, id)
    book = Database_control.get_book(cursor, id)
    chapter = Database_control.get_chapter(cursor, id)
    bible_version = Database_control.get_bible_version(cursor, id) 
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        # Full version name (no acronym)
        try:
            bible_version = dict_api_acr2ver[bible_version]
        except:
            bible_version = "akjv"

        if status==1:
            status='✅'
        else:
            status='❌'

        info_text = "📒 Information \n📚 Subscribed: \t"+status+"\n🌎 Language: \t"+str(language)+"\n📖 Current Bible Book: \t"+str(book)+"\n📑 Current Chapter: \t"+str(chapter)+"\n📕 Current Bible Version: \t"+str(bible_version)
        send_translated_message(m.chat.id, info_text, language)  # Send info text
        show_mainkeyboard(m)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")        
        command_start(m)



# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    id = m.chat.id
    connection, cursor = Database_control.create_db()
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        help_text = "Avaliable commands: \n\n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": " + commands[key] + "\n"
        send_translated_message(id, help_text, language)  # send the generated help page
        show_mainkeyboard(m)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        command_start(m)


def show_mainkeyboard(m):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for each in range(0,len(list(commands.keys()))):
        start_markup.row("/"+list(commands.keys())[each])

    start_markup.row("/hide_keyboard")
    
    bot.send_message(m.from_user.id, "⌨️❔", reply_markup=start_markup)


# Hide keyboard
@bot.message_handler(commands=['hide_keyboard'])
def command_hide(message):
    # bot.send_chat_action(id, 'typing')
    hide_markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


# subscribe/ unsubscribe
@bot.message_handler(commands=['subscribe'])
def command_subscribe(m):
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
    current_status = Database_control.get_status(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)

    if verify_id:
        if current_status==1:
            new_status=0
        else:
            new_status=1

        Database_control.set_status(connection, cursor, new_status, id)
        language = Database_control.get_language(cursor, id)
        Database_control.close_db(connection)

        if new_status==1:
            status='✅'
        else:
            status='❌' 

        text = "Subscription: \t"+status 
        send_translated_message(id, text, language)  # send the generated text
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        Database_control.close_db(connection)
        command_start(m)

    

# set language page
@bot.message_handler(commands=['language'])
def command_language(m):
    command_hide(m)
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
    Database_control.set_mod_language(connection, cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        send_translated_message(id, "Type your new language", language)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        command_start(m)

    
# set book page
@bot.message_handler(commands=['choose_book'])
def command_book(m):
    command_hide(m)
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
    Database_control.set_mod_book(connection, cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        send_translated_message(id, "Type the desired bible book", language)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        command_start(m)


# set current chapter
@bot.message_handler(commands=['choose_chapter'])
def command_chapter(m):
    command_hide(m)
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
    Database_control.set_mod_chapter(connection, cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)
    Database_control.close_db(connection)

    if verify_id:
        send_translated_message(id, "Type the number of the desired chapter to start with", language)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        command_start(m)
    

@bot.message_handler(commands=['bible_version'])
def command_bible_version(m):
    command_hide(m)
    id = m.chat.id
    
    connection, cursor = Database_control.create_db()
        
    Database_control.set_mod_bible_version(connection, cursor, id)
    language = Database_control.get_language(cursor, id)
    verify_id = Database_control.verify_id(cursor, id)

    if verify_id:
        if language in dict_api_version.keys():
            versions = dict_api_version[language] + dict_api_version["English"]
        else:
            versions = dict_api_version["English"]

        version_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

        for each in range(0,len(versions)):
            version_markup.row(versions[each])
    
        Database_control.set_mod_default(connection, cursor, id)
        Database_control.set_mod_bible_version(connection, cursor, id)
        Database_control.close_db(connection)
            
        bot.send_message(m.from_user.id, "⌨️", reply_markup=version_markup)
    else:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        Database_control.close_db(connection)
        command_start(m)
    
    
# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    id = m.chat.id
        
    connection, cursor = Database_control.create_db()

    if Database_control.verify_id(cursor, id) == False:
        send_translated_message(m.chat.id, "You are a new user. Check what I can do at /start")
        Database_control.close_db(connection)
        command_start(m)
    else:
        # TODO - put all in a tuple instead single queries - optimize db queries
        lang_selection = Database_control.get_mod_language(cursor, id)
        bible_book_selection = Database_control.get_mod_book(cursor, id)
        chapter_selection = Database_control.get_mod_chapter(cursor, id)
        bible_version_selection = Database_control.get_mod_bible_version(cursor, id)

        verse = Database_control.get_verse(cursor, id)
        origin_language = Database_control.get_language(cursor, id)  
        bible_version = Database_control.get_bible_version(cursor, id)
        
          
        if lang_selection == True:
            language = verify_language(m.text)
            Database_control.set_language(connection, cursor, language, id)
            Database_control.set_mod_language(connection, cursor, id)
           
            if language in dict_api_version.keys():
                Database_control.set_bible_version(connection, cursor, dict_api_ver2acr[dict_api_version[language][0]], id)
            else:
                Database_control.set_bible_version(connection, cursor, 'akjv', id)

            send_translated_message(m.chat.id, "The selected language is "+ language, origin_language)  
            Database_control.set_mod_default(connection, cursor, id)
            Database_control.close_db(connection)
            show_mainkeyboard(m)

        elif verse == True:
            send_translated_message(id, "Accepted request - Searching ...", origin_language) 
            message = m.text
            
            try:
                if origin_language in lang_ver_transl:
                    if origin_language != 'English':
                        n_message = Bible.translate_message(message, language="English", src=origin_language)
                    else:
                        n_message = message

                    if n_message.split(":")[-1][0] == " ":
                        n_message = "".join([n_message.split(":")[:-1][0],":","".join(n_message.split(":")[-1][1:].split(" "))])

                    response = Bible.get_message(n_message, bible_version)

                else:
                    n_message = Bible.translate_message(message, language="English", src=origin_language)

                    if n_message.split(":")[-1][0] == " ":
                        n_message = "".join([n_message.split(":")[:-1][0],":","".join(n_message.split(":")[-1][1:].split(" "))])

                    response = Bible.get_message(n_message, bible_version)
                    response = Bible.translate_message(response, origin_language)

                Database_control.set_verse(connection, cursor, id)

            except (Exception) as exception:
                logging.critical("In message handler - Exception: ", exception)

            response = [i for i in telebot.util.split_string(response, 3000)]
            for each_message in response:
                send_translated_message(id, each_message, origin_language)
            
            Database_control.set_mod_default(connection, cursor, id)
            Database_control.close_db(connection)
            show_mainkeyboard(m)

        elif bible_book_selection == True:
            message = m.text
            command_hide(m)

            if origin_language in (list(lang_ver_transl)+list(lang_transl)):
                if origin_language != 'English':
                    n_message = Bible.translate_message(message, language="English", src=origin_language)
                else:
                    n_message = message
                
                book = Bible.verify_book(n_message)

            else:
                send_translated_message(m.chat.id, "As your language is not available, please write in English", origin_language)  
                n_message = message
                
            book = Bible.verify_book(n_message)

            Database_control.set_book(connection, cursor, book, id)
            Database_control.set_mod_book(connection, cursor, id)
            Database_control.set_mod_default(connection, cursor, id)
           
            send_translated_message(m.chat.id, "The selected Book is "+ book, origin_language)  
            Database_control.close_db(connection)
            show_mainkeyboard(m)
        
        elif chapter_selection == True:
            message = m.text
            book = Database_control.get_book(cursor, id)

            if message.isnumeric():
                if (Bible.verify_book_chapter(book, message) == True) and (int(message) >= 1):
                    Database_control.set_chapter(connection, cursor, message, id)
                    send_translated_message(m.chat.id, "The selected chapter is "+ message, origin_language)  
                else:
                    send_translated_message(m.chat.id, "This chapter doesn't exist for the book of "+book+". \nChapter 1 selected.", origin_language)
                    message = "1"
                    Database_control.set_chapter(connection, cursor, "1", id)

            else:
                message = "1"
                send_translated_message(m.chat.id, "This is not a number. \nChapter 1 selected.", origin_language)
                Database_control.set_chapter(connection, cursor, "1", id)
            
            Database_control.set_mod_book(connection, cursor, id)
            Database_control.set_mod_default(connection, cursor, id)
            Database_control.close_db(connection)
            show_mainkeyboard(m)


        elif bible_version_selection == True:
            message = m.text
            command_hide(m)
            version = verify_version(message)
            acr = dict_api_ver2acr[version]
            Database_control.set_bible_version(connection, cursor, acr, id)
            Database_control.set_mod_default(connection, cursor, id)
            Database_control.close_db(connection)
            show_mainkeyboard(m)


        else:
            send_translated_message(m.chat.id, "I don't understand. \nTry the help page at '/help'", origin_language)
            Database_control.set_mod_default(connection, cursor, id)
            Database_control.close_db(connection)
            show_mainkeyboard(m)

    Database_control.close_db(connection)


########################################################################
################            MAIN FUNCTION             ##################
########################################################################
#telebot.apihelper.READ_TIMEOUT = 1
if __name__ == "__main__":       
    # bot.polling(none_stop=True, timeout=30)
    while True:
        try: 
            log.info('Starting bot')
            bot.polling(none_stop=True, timeout=30)
        except Exception as err:
            log.error("Bot polling error: {0}".format(err.args))
            bot.stop_polling()
            time.sleep(60)

            
