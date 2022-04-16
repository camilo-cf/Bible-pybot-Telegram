[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=bugs)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=coverage)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=camilo-cf_Bible-pybot-Telegram&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=camilo-cf_Bible-pybot-Telegram)
[![CodeFactor](https://www.codefactor.io/repository/github/camilo-cf/bible-pybot-telegram/badge)](https://www.codefactor.io/repository/github/camilo-cf/bible-pybot-telegram)
[![Maintainability](https://api.codeclimate.com/v1/badges/39e59bfbd5a36e37a24f/maintainability)](https://codeclimate.com/github/camilo-cf/Bible-pybot-Telegram/maintainability)
[![codecov](https://codecov.io/gh/camilo-cf/Bible-pybot-Telegram/branch/main/graph/badge.svg?token=53XILYFINM)](https://codecov.io/gh/camilo-cf/Bible-pybot-Telegram)
[![Known Vulnerabilities](https://snyk.io/test/github/camilo-cf/bible-pybot-telegram/badge.svg)](https://snyk.io/test/github/camilo-cf/bible-pybot-telegram)
[![Codecov](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/codecov_main.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/codecov_main.yml)
[![Docker Snyk](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/docker_snyk.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/docker_snyk.yml)
[![Pylint](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/pylint.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/pylint.yml)
[![Python Snyk](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/python_snyk.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/python_snyk.yml)
[![Sphinx](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/sphinx_action.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/sphinx_action.yml)
[![pages-build-deployment](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/pages/pages-build-deployment)
[![Mypy](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/mypy.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/mypy.yml)
[![SonarCloud](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/sonarcloud.yml/badge.svg)](https://github.com/camilo-cf/Bible-pybot-Telegram/actions/workflows/sonarcloud.yml)

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

TBD
