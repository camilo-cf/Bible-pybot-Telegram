"""
    Constants file for the project.
"""
import os

BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua',
         'Judges', 'Ruth', '1Samuel', '2Samuel', '1Kings', '2Kings', '1Chronicles',
         '2Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs',
         'Ecclesiastes', 'SongofSolomon', 'Isaiah', 'Jeremiah', 'Lamentations',
         'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah',
         'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
         'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1Corinthians',
         '2Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians',
         '1Thessalonians', '2Thessalonians', '1Timothy', '2Timothy', 'Titus',
         'Philemon', 'Hebrews', 'James', '1Peter', '2Peter', '1John', '2John',
         '3John', 'Jude', 'Revelation']

DICT_BOOKS = dict(zip(BOOKS, range(1, len(BOOKS)+1)))

JSON_API_URL = "https://getbible.net/json?passage="
JSON_API_URL_2PART = "&version="

# Telegram TOKEN
TOKEN = os.getenv("BOT_TOKEN")

# command description used in the "help" command
COMMANDS = {
    'start': '☝ Know what can I do',
    'send_chapter': '📧 Send now the chapter to read',
    'verse': '⛪ Request a Bible passage',
    'information': '📒 Know your information and settings for this bot',
    'help': '❔ Gives you information about the available commands',
    'subscribe': '📚 Receive 1 Bible chapter every day at a given time or Cancel it',
    'language': '🌎 Select your preferred language',
    'choose_book': '📖 Select the current bible book you are reading',
    'choose_chapter': '📑 Select the current chapter you want to start reading',
    'bible_version': '📕 Select the bible version'
}


# Available Languages and Versions in the API
f = open(os.path.join(os.getcwd(), "src/utils/", "languages_api.txt"), "r")
bible_api_list = []
for x in f:
    bible_api_list.append(x[4:])
f.close()

dict_api_version = {}
languages_api = []

for each_language in bible_api_list:
    language = each_language.split(":")[0]
    languages_api.append(language)
    dict_api_version[language] = []

acronyms_api = []
version_api = []

for each in bible_api_list:
    language = each.split(":")[0]
    acronym = each.split("(")[-1].split(")")[0]
    version = each.split(":")[1].split(acronym)[0][:-1]

    acronyms_api.append(acronym)
    version_api.append(version)

    dict_api_version[language].append(version)

dict_api_ver2acr = dict(zip(version_api, acronyms_api))
dict_api_acr2ver = dict(zip(acronyms_api, version_api))
unique_languages_api = set(languages_api)

# Available translation languages
f = open(os.path.join(os.getcwd(), "src/utils/", "language_translate.txt"), "r")
languages_translation = []
for each in f:
    languages_translation.append(each.split("\n")[0])
f.close()

# Languages comparison
languages_translation_set = set(languages_translation)
lang_ver_transl = languages_translation_set.intersection(unique_languages_api)
lang_transl = languages_translation_set.difference(unique_languages_api)