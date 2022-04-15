from email import message
import logging as log
import sys
from telebot.util import split_string as split_string

sys.path.append("./src/")

from utils import bible as Bible
from utils import constants as K
from utils import queries as Q
from utils import database_control as Database_control
import utils.validations as validations


class TelegramPages:
    """Class to interface all the bot behavior"""

    def __init__(self):
        """Initializes the class and creates a connection on the default database location."""
        self.db = Database_control.UsersDB()

    def start(self, user_id: str, user_name: str) -> str:
        """Bot's start message

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            user_name (str):
                Name of the user

        Returns:
            A string with a message
        """
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0
        if not exist:
            self.db.execute_query(Q.ADD_USER.format(user_id, user_name))
            language = "English"
        else:
            language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][
                0
            ]

        return validations.translate_message(K.START_MSG, language=language)

    def send_chapter(
        self,
        user_id: str,
    ) -> list:
        """Send chapter functionality

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A list of strings with the next chapter
        """
        book = self.db.fetch_query(Q.GET_BOOK.format(user_id))[0][0]
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        chapter = self.db.fetch_query(Q.GET_CHAPTER.format(user_id))[0][0]
        bible_version = self.db.fetch_query(
            Q.GET_BIBLE_VERSION.format(user_id)
        )[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if exist:
            chapter2send = " ".join([book, str(chapter)])
            chp_native = chapter2send
            try:
                if (language in K.lang_ver_transl) and (
                    K.dict_api_acr2ver[bible_version]
                    in K.dict_api_version[language]
                ):
                    response = Bible.get_message(chapter2send, bible_version)
                else:
                    chapter2send = validations.translate_message(
                        chapter2send, language="English", src=language
                    )
                    response = validations.translate_message(
                        Bible.get_message(
                            chapter2send,
                            bible_version,
                        ),
                        language,
                        "English",
                    )
            except Exception:
                response = validations.translate_message(
                    K.ERROR, language, "English"
                )
                log.critical(f"{Exception}")

            message = [f"{chp_native} ({chapter2send})"] + list(
                split_string(response, 3000)
            )

            # Update next chapter in the db
            next_chapter = Bible.get_next_chapter(chapter2send)
            next_book = next_chapter.split(" ")[0]
            next_chapter = next_chapter.split(" ")[1]

            self.db.execute_query(Q.SET_BOOK.format(next_book, user_id))
            self.db.execute_query(Q.SET_CHAPTER.format(next_chapter, user_id))
            self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        else:
            message = [
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            ]
        return message

    def verse(
        self,
        user_id: str,
    ) -> str:
        """Start the verse process

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str message requesting the verse to be sent
        """
        self.db.execute_query(Q.SET_VERSE.format(True, user_id))
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        return (
            [
                validations.translate_message(
                    single_mesage, language, "English"
                )
                for single_mesage in K.VERSE_MSG
            ]
            if exist
            else validations.translate_message(
                K.NEW_USR_ERROR, language, "English"
            )
            + K.START_FN
        )

    def information(
        self,
        user_id: str,
    ) -> str:
        """Send user's information

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str with the user information
        """
        book = self.db.fetch_query(Q.GET_BOOK.format(user_id))[0][0]
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        chapter = self.db.fetch_query(Q.GET_CHAPTER.format(user_id))[0][0]
        bible_version = self.db.fetch_query(
            Q.GET_BIBLE_VERSION.format(user_id)
        )[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if exist:
            try:
                bible_version = K.dict_api_acr2ver[bible_version]
            except Exception:
                bible_version = "akjv"

            return validations.translate_message(
                K.INFO_MSG.format(language, book, chapter, bible_version),
                language,
                "English",
            )

        else:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )

    def help(
        self,
        user_id: str,
    ) -> str:
        """Send the bot's help

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str wit the help message
        """
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if not exist:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )
        message = (
            validations.translate_message(K.HELP_MSG, language, "English")
            + "\n\n"
        )
        for key in K.COMMANDS:
            message += (
                "/"
                + key
                + ": "
                + validations.translate_message(
                    K.COMMANDS[key], language, "English"
                )
                + "\n"
            )
        return message

    def language(
        self,
        user_id: str,
    ) -> str:
        """Starts the change of language

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str message requesting for the new language
        """
        self.db.execute_query(Q.SET_MOD_LANGUAGE.format(True, user_id))
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if exist:
            return validations.translate_message(
                K.LANG_MSG, language, "English"
            )
        else:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )

    def book(
        self,
        user_id: str,
    ) -> str:
        """Starts the change of Bible's book

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str message requesting for the new book
        """
        self.db.execute_query(Q.SET_MOD_BOOK.format(True, user_id))
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if exist:
            return validations.translate_message(
                K.BOOK_MSG, language, "English"
            )
        else:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )

    def chapter(
        self,
        user_id: str,
    ) -> str:
        """Starts the change of Bible's Book chapter

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A str message requesting for the new book's chapter number
        """
        self.db.execute_query(Q.SET_MOD_CHAPTER.format(True, user_id))
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        if exist:
            return validations.translate_message(
                K.CHAPTER_MSG, language, "English"
            )
        else:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )

    def bible_version(
        self,
        user_id: str,
    ) -> tuple:
        """Starts the change of Bible's version

        Args:
            user_id (str):
                ID of the user the bot is interacting with

        Returns:
            A tuple with:
                A str message requesting for the new book's chapter number
                The available versions
        """
        self.db.execute_query(Q.SET_MOD_BIBLE_VERSION.format(True, user_id))
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0

        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        self.db.execute_query(Q.SET_MOD_BIBLE_VERSION.format(True, user_id))

        if not exist:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN,
                [],
            )
        versions = (
            K.dict_api_version[language] + (K.dict_api_version["English"])
            if language in K.dict_api_version
            else K.dict_api_version["English"]
        )

        return (
            validations.translate_message(K.CHAPTER_MSG, language, "English"),
            versions,
        )

    def default(
        self,
        user_id: str,
        income_text: str,
    ) -> list:
        """Main function to interact with default text.

        This function can handle the SET of:
            - Language selection
            - Bible book selection
            - Bible version selection
            - Chapter selection
            - Send a desired verse

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            List of strings with the required information
        """
        exist = len(self.db.fetch_query(Q.VERIFY_ID.format(user_id))) != 0
        language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[0][0]
        if exist:
            lang_selection = (
                self.db.fetch_query(Q.GET_MOD_LANGUAGE.format(user_id))[0][0]
                == "True"
            )
            bible_book_selection = (
                self.db.fetch_query(Q.GET_MOD_BOOK.format(user_id))[0][0]
                == "True"
            )
            chapter_selection = (
                self.db.fetch_query(Q.GET_MOD_CHAPTER.format(user_id))[0][0]
                == "True"
            )
            bible_version_selection = (
                self.db.fetch_query(Q.GET_MOD_BIBLE_VERSION.format(user_id))[
                    0
                ][0]
                == "True"
            )
            send_verse = (
                self.db.fetch_query(Q.GET_VERSE.format(user_id))[0][0]
                == "True"
            )

            if lang_selection:
                return [self.set_language(user_id, income_text)]
            elif send_verse:
                return self.return_verse(user_id, income_text)
            elif bible_book_selection:
                return [self.set_bible_book(user_id, income_text)]
            elif bible_version_selection:
                return [self.set_bible_version(user_id, income_text)]
            elif chapter_selection:
                return [self.set_chapter_selection(user_id, income_text)]
            else:
                self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
                return [
                    validations.translate_message(
                        K.NO_UNDERSTAND, language, "English"
                    )
                    + "'/help'"
                ]
        else:
            return (
                validations.translate_message(
                    K.NEW_USR_ERROR, language, "English"
                )
                + K.START_FN
            )

    def set_language(self, user_id: str, income_text: str) -> str:
        """Set the desired language

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            List of strings with the selection language message
        """
        language = validations.verify_language(income_text)
        self.db.execute_query(Q.SET_LANGUAGE.format(language, user_id))
        self.db.execute_query(Q.SET_MOD_LANGUAGE.format(False, user_id))

        if language in K.dict_api_version:
            self.db.execute_query(
                Q.SET_BIBLE_VERSION.format(
                    K.dict_api_ver2acr[K.dict_api_version[language][0]],
                    user_id,
                )
            )
        else:
            self.db.execute_query(Q.SET_BIBLE_VERSION.format("akjv", user_id))

        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        return validations.translate_message(
            K.SELECTED_LANG.format(language), language, "English"
        )

    def return_verse(self, user_id: str, income_text: str) -> list:
        """Return the desired verse

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            List of strings with the required information
        """
        original_income = income_text
        try:
            origin_language = self.db.fetch_query(
                Q.GET_LANGUAGE.format(user_id)
            )[0][0]
            bible_version = self.db.fetch_query(
                Q.GET_BIBLE_VERSION.format(user_id)
            )[0][0]
            if origin_language in K.lang_ver_transl:
                if origin_language != "English":
                    income_text = validations.translate_message(
                        income_text, language="English", src=origin_language
                    )

                if income_text.split(":")[-1][0] == " ":
                    income_text = "".join(
                        [
                            income_text.split(":")[:-1][0],
                            ":",
                            "".join(income_text.split(":")[-1][1:].split(" ")),
                        ]
                    )
                response = (
                    f"{original_income} ({income_text}) \n"
                    + Bible.get_message(income_text, bible_version)
                )

            else:
                income_text = Bible.translate_message(
                    income_text, language="English", src=origin_language
                )

                if income_text.split(":")[-1][0] == " ":
                    income_text = "".join(
                        [
                            income_text.split(":")[:-1][0],
                            ":",
                            "".join(income_text.split(":")[-1][1:].split(" ")),
                        ]
                    )
                response = (
                    f"{original_income} ({income_text}) \n"
                    + validations.translate_message(
                        validations.get_message(income_text, bible_version),
                        origin_language,
                    )
                )

        except Exception:
            log.critical(Exception)

        self.db.execute_query(Q.SET_VERSE.format(False, user_id))
        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        return list(split_string(response, 3000))

    def set_bible_book(self, user_id: str, income_text: str) -> str:
        """Set the desired Bible book

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            A string with the confirmation message
        """
        origin_language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[
            0
        ][0]

        self.db.execute_query(Q.SET_MOD_BOOK.format(False, user_id))
        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        if origin_language in list(K.lang_ver_transl) + list(K.lang_transl):
            if origin_language != "English":
                income_text = validations.translate_message(
                    f"{income_text} 1.",
                    language="English",
                    src=origin_language,
                )[:-3]
            book = validations.verify_book(income_text)
            self.db.execute_query(Q.SET_BOOK.format(book, user_id))
            self.db.execute_query(Q.SET_CHAPTER.format(1, user_id))
            return validations.translate_message(
                K.SELECT_BOOK.format(book), origin_language
            )
        else:
            return validations.translate_message(
                K.ERROR_SELECT_BOOK, origin_language
            )

    def set_bible_version(self, user_id: str, income_text: str) -> str:
        """Set the Bible's version

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            A string with the confirmation message
        """
        origin_language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[
            0
        ][0]
        version = validations.verify_version(income_text)
        version_key = K.dict_api_ver2acr[
            validations.verify_version(income_text)
        ]
        self.db.execute_query(Q.SET_BIBLE_VERSION.format(version_key, user_id))
        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        return validations.translate_message(
            K.SELECT_VERSION.format(version), origin_language
        )

    def set_chapter_selection(self, user_id: str, income_text: str) -> str:
        """_summary_

        Args:
            user_id (str):
                ID of the user the bot is interacting with

            income_text (str):
                A str with the user's message to be processed

        Returns:
            A string with the confirmation message
        """
        book = self.db.fetch_query(Q.GET_BOOK.format(user_id))[0][0]
        origin_language = self.db.fetch_query(Q.GET_LANGUAGE.format(user_id))[
            0
        ][0]

        if income_text.isnumeric():
            if (
                validations.verify_book_chapter(book, income_text) == True
            ) and (int(income_text) >= 1):
                self.db.execute_query(
                    Q.SET_CHAPTER.format(income_text, user_id)
                )
                return_msg = validations.translate_message(
                    K.SELECT_CHAPTER.format(income_text), origin_language
                )
            else:
                income_text = "1"
                self.db.execute_query(
                    Q.SET_CHAPTER.format(income_text, user_id)
                )
                return_msg = validations.translate_message(
                    K.SELECT_CHAPTER_ERROR.format(book), origin_language
                )

        else:
            income_text = "1"
            self.db.execute_query(Q.SET_CHAPTER.format(income_text, user_id))
            return_msg = validations.translate_message(
                K.SELECT_CHAPTER_ERROR_NAN, origin_language
            )

        self.db.execute_query(Q.SET_MOD_BOOK.format(False, user_id))
        self.db.execute_query(Q.SET_MOD_DEFAULT.format(user_id))
        return return_msg
