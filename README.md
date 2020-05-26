# cocoa-bot
A Python bot for the Slugfest Discord server

## External Dependencies
* Install external dependencies by running `pip install -r requirements.txt`.
* [**python-dotenv**](https://pypi.org/project/python-dotenv) [![PyPI version](https://badge.fury.io/py/python-dotenv.svg)](https://badge.fury.io/py/python-dotenv)
* [**discord.py**](https://pypi.org/project/discord.py) [![PyPI version](https://badge.fury.io/py/discord.py.svg)](https://badge.fury.io/py/discord.py)

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
* Install any needed dependencies by running `pip install -r requirements.txt`.
* Create a file named `.env` in the project root directory.
* Insert the environment variables relevant to your bot and server as such:
  * ```
    COCOA_BOT_TOKEN={YOUR DISCORD BOT TOKEN}
    COCOA_DB={PATH TO DATABASE FILE}
    COCOA_TABLE={NAME OF TABLE WITHIN DATABASE}
    COCOA_CHANNEL={INTEGER REPRESENTING CHANNEL ID}
    ```
* Run `bot.py`.
