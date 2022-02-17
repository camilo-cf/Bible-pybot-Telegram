"""
    Constants file for the project.
"""
import os

BOOKS = [
    'Genesis',
    'Exodus',
    'Leviticus',
    'Numbers',
    'Deuteronomy',
    'Joshua',
    'Judges',
    'Ruth',
    '1Samuel',
    '2Samuel',
    '1Kings',
    '2Kings',
    '1Chronicles',
    '2Chronicles',
    'Ezra',
    'Nehemiah',
    'Esther',
    'Job',
    'Psalms',
    'Proverbs',
    'Ecclesiastes',
    'SongofSolomon',
    'Isaiah',
    'Jeremiah',
    'Lamentations',
    'Ezekiel',
    'Daniel',
    'Hosea',
    'Joel',
    'Amos',
    'Obadiah',
    'Jonah',
    'Micah',
    'Nahum',
    'Habakkuk',
    'Zephaniah',
    'Haggai',
    'Zechariah',
    'Malachi',
    'Matthew',
    'Mark',
    'Luke',
    'John',
    'Acts',
    'Romans',
    '1Corinthians',
    '2Corinthians',
    'Galatians',
    'Ephesians',
    'Philippians',
    'Colossians',
    '1Thessalonians',
    '2Thessalonians',
    '1Timothy',
    '2Timothy',
    'Titus',
    'Philemon',
    'Hebrews',
    'James',
    '1Peter',
    '2Peter',
    '1John',
    '2John',
    '3John',
    'Jude',
    'Revelation']

DICT_BOOKS = dict(zip(BOOKS, range(1, len(BOOKS) + 1)))

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
    'bible_version': '📕 Select the bible version'}

TEST_BOOK_CHAPTERS = {
    'Genesis': 50,
    'Exodus': 40,
    'Leviticus': 27,
    'Numbers': 36,
    'Deuteronomy': 34,
    'Joshua': 24,
    'Judges': 21,
    'Ruth': 4,
    '1 Samuel': 31,
    '2 Samuel': 24,
    '1 Kings': 22,
    '2 Kings': 25,
    '1 Chronicles': 29,
    '2 Chronicles': 36,
    'Ezra': 10,
    'Nehemiah': 13,
    'Esther': 10,
    'Job': 42,
    'Psalms': 150,
    'Proverbs': 31,
    'Ecclesiastes': 12,
    'Song of Solomon': 8,
    'Isaiah': 66,
    'Jeremiah': 52,
    'Lamentations': 5,
    'Ezekiel': 48,
    'Daniel': 12,
    'Hosea': 14,
    'Joel': 3,
    'Amos': 9,
    'Obadiah': 1,
    'Jonah': 4,
    'Micah': 7,
    'Nahum': 3,
    'Habakkuk': 3,
    'Zephaniah': 3,
    'Haggai': 2,
    'Zechariah': 14,
    'Malachi': 4,
    'Matthew': 28,
    'Mark': 16,
    'Luke': 24,
    'John': 21,
    'Acts': 28,
    'Romans': 16,
    '1 Corinthians': 16,
    '2 Corinthians': 13,
    'Galatians': 6,
    'Ephesians': 6,
    'Philippians': 4,
    'Colossians': 4,
    '1 Thessalonians': 5,
    '2 Thessalonians': 3,
    '1 Timothy': 6,
    '2 Timothy': 4,
    'Titus': 3,
    'Philemon': 1,
    'Hebrews': 13,
    'James': 5,
    '1 Peter': 5,
    '2 Peter': 3,
    '1 John': 5,
    '2 John': 1,
    '3 John': 1,
    'Jude': 1,
    'Revelation': 22}


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
f = open(
    os.path.join(
        os.getcwd(),
        "src/utils/",
        "language_translate.txt"),
    "r")
languages_translation = []
for each in f:
    languages_translation.append(each.split("\n")[0])
f.close()

# Languages comparison
languages_translation_set = set(languages_translation)
lang_ver_transl = languages_translation_set.intersection(unique_languages_api)
lang_transl = languages_translation_set.difference(unique_languages_api)
