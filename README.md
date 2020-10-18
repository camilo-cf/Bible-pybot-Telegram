# Bible-pybot-Telegram

Here I present the code of a Bible bot that can be found on telegram on [t.me/Bible_pybot](t.me/Bible_pybot). I will try to keep this bot working (on a raspberry pi) for my personal use (push me to read 1 chapter of the Bible daily); feel free to use it and report issues.

This is a project developed for educational/ personal purposes. Use this bot under your responsibility, no warranties.

subscribe here [t.me/Bible_pybot](t.me/Bible_pybot) in Telegram.

### Screen record usage
<p align="center">
<img src="SupportFiles/Screeenrecord.gif" width="200"/>
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

# Requirements

I worked mainly with the next libraries (you can install them using pip):

```
pyTelegramBotAPI == 3.6.6
numpy == 1.17.1
googletrans ==  3.0.0
requests == 2.22.0
```
Don't forget to add your telegram TOKEN to your config.txt file.

# Deployment

You can deploy it as you want Heroku, pythoneverywhere, your server etc.

In my case, I deployed it on a raspberry pi zero. I used crontab to schedule the tasks (run the main.py on boot to keep the service alive and the daily chapter to be sent daily at 0:00 GTM+1).

Feel free to contact me if you have any doubt.