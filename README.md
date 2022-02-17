[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![CodeFactor](https://www.codefactor.io/repository/github/camilo-cf/bible-pybot-telegram/badge)](https://www.codefactor.io/repository/github/camilo-cf/bible-pybot-telegram)
[![Maintainability](https://api.codeclimate.com/v1/badges/39e59bfbd5a36e37a24f/maintainability)](https://codeclimate.com/github/camilo-cf/Bible-pybot-Telegram/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/39e59bfbd5a36e37a24f/test_coverage)](https://codeclimate.com/github/camilo-cf/Bible-pybot-Telegram/test_coverage)
[![codecov](https://codecov.io/gh/camilo-cf/Bible-pybot-Telegram/branch/master/graph/badge.svg?token=53XILYFINM)](https://codecov.io/gh/camilo-cf/Bible-pybot-Telegram)
[![Known Vulnerabilities](https://snyk.io/test/github/camilo-cf/bible-pybot-telegram/badge.svg)](https://snyk.io/test/github/camilo-cf/bible-pybot-telegram)


# Bible-pybot-Telegram

Here I present the code of a Bible bot that can be found on telegram on [https://t.me/Bible_pybot](https://t.me/Bible_pybot). I will try to keep this bot working (on a raspberry pi) for my personal use (push me to read 1 chapter of the Bible daily); feel free to use it and report issues.

This is a project developed for educational/ personal purposes. Use this bot under your responsibility, no warranties.

subscribe here [https://t.me/Bible_pybot](https://t.me/Bible_pybot) in Telegram.

### Screen record
<p align="center">
<img src="doc/Screeenrecord.gif" width="200"/>
</p>

## Features

* Free use Telegram bot.
* A lot of languages for interaction and get the Bible passages (Set your language).
* Get any Bible passage (when you want).
* Get a daily chapter in consecutive order (set the current book and chapter you are reading, or start from Genesis 1).
* Change the Bible version you are reading (only available the provided by the API).
* Subscribe/Unsubscribe to the daily chapter list.
* Get your current status in the service (language, subscription status, bible version, current chapter/book)


# Technical Details

This project uses the http://getbible.net API to gather the bible verses on different bible versions and languages.

A simple database in SQLite is used to save the users' id, preferences, current bible version, language, subscription status, current book, and current chapter.

The frontend of this bot is in telegram using the **pyTelegramBotAPI** library. If you want to deploy it yourself, add the API token in the config.txt file (Get it from the BotFather in Telegram; it is very easy).

The translation are done with the **googletrans** library.

# Deployment

TDB
