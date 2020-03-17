# cocoa-bot
A Python bot for the Slugfest Discord server

## External Dependencies
* [**python-dotenv**](https://pypi.org/project/python-dotenv) [![PyPI version](https://badge.fury.io/py/python-dotenv.svg)](https://badge.fury.io/py/python-dotenv) — `pip install python-dotenv==0.12.0`
* [**discord.py**](https://pypi.org/project/discord.py) [![PyPI version](https://badge.fury.io/py/discord.py.svg)](https://badge.fury.io/py/discord.py) — `pip install discord.py=1.3.2`

## Usage
### In a text channel:
```
No Category:
  cocoa       Yells Cocoa! into your text channel.
  cocoa-count Report the amount of times this @'ed user has said 'cocoa'
  help        Shows this message

Type !help command for more info on a command.
You can also type !help category for more info on a category.
```
### Deploying on a machine:
* Create a file named `.env` in the same directory as `bot.py`.
* Insert the environment variables relevant to your bot and server as such:
  * ```
    COCOA_BOT_TOKEN={YOUR DISCORD BOT TOKEN}
    COCOA_DB={PATH TO DATABASE FILE}
    COCOA_TABLE={NAME OF TABLE WITHIN DATABASE}
    COCOA_CHANNEL={INTEGER REPRESENTING CHANNEL ID}
    ```
* Run `bot.py`.
