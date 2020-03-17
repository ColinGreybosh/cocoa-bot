import os
import re
import sqlite3
import asyncio
import datetime

from dotenv import load_dotenv
from urllib.request import pathname2url
from discord import Message
from discord import Member
from discord.ext import commands

load_dotenv()

# database rows have values of (id int, count int)
COCOA_REGEX = re.compile('[cC]+[oO]+[cC]+[oO]+[aA]+')
COCOA_DB = os.getenv('COCOA_DB')
COCOA_TABLE = os.getenv('COCOA_TABLE')
COCOA_CHANNEL = os.getenv('COCOA_CHANNEL')

VERBOSE = False

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    conn = sqlite3.connect(COCOA_DB)
    c = conn.cursor()
    users_to_add = set([member.id for member in bot.guilds.pop().members])
    for row in c.execute(f'SELECT * FROM {COCOA_TABLE}'):
        user_id, count = row
        users_to_add.remove(user_id)
    for user_id in users_to_add:  # Add any new guild members to the database
        c.execute(f'INSERT INTO {COCOA_TABLE} VALUES ({user_id}, 0)')
    conn.commit()
    conn.close()

    while True:
        friday = 4
        saturday = 5
        weekday, hour, minute, second = get_weekday_and_hms()
        if VERBOSE:
            print(f'{weekday} {hour} {minute} {second}')
        if weekday != friday and weekday != saturday:
            if hour == 23 and minute == 0 and second == 0:
                cocoa_channel = bot.get_channel(COCOA_CHANNEL)
                await cocoa_channel.send('☕ COOOOOOOOOOOCOOOOOOOOOOOOOOOOAAAAAAAA!!! ☕')
        await asyncio.sleep(1)


@bot.event
async def on_member_join(ctx: commands.Context, member: Member):
    conn = sqlite3.connect(COCOA_DB)
    c = conn.cursor()
    joined_user_id = member.id
    for user_id in c.execute(f'SELECT user_id FROM {COCOA_TABLE}'):
        if user_id == joined_user_id:
            return
    c.execute(f'INSERT INTO {COCOA_TABLE} VALUES ({joined_user_id}, 0)')
    conn.commit()
    conn.close()


@bot.command(name='cocoa', help='Yells Cocoa! into your text channel.')
async def on_message(ctx: commands.Context):
    """Yells cocoa into your text channel."""
    await ctx.send('☕ COOOOOOOOOOOCOOOOOOOOOOOOOOOOAAAAAAAA!!! ☕')


@bot.command(name='cocoa-count', help='Report the amount of times this @\'ed user has said \'cocoa\'')
async def on_message(ctx: commands.Context, user: str):
    """Report the amount of times a given @'ed user has yelled 'cocoa'.

    Keyword arguments:
    user -- the user to report a cocoa count for
    """
    if user.startswith('<@!') and user.endswith('>'):
        conn = sqlite3.connect(COCOA_DB)
        c = conn.cursor()
        user_id = int(user[3:len(user) - 1])
        try:
            display_name = get_display_name_by_id(bot, user_id)
            c.execute(f'SELECT count FROM {COCOA_TABLE} WHERE user_id={user_id}')
            cocoa_count = c.fetchone()[0]

            await ctx.send(f'{display_name} has said COCOA on this server {cocoa_count} '
                           f'{"time" if cocoa_count == 1 else "times"}.')
        except ValueError as e:
            error_msg = ''
            for arg in e.args:
                error_msg += arg
            await ctx.send(f'Error! `{error_msg}`')
        except Exception as e:
            error_msg = ''
            for arg in e.args:
                error_msg += arg
            await ctx.send(f'Error! `{error_msg}`')
    else:
        await ctx.send('Error! `You must @ a user to check their cocoa count.`')


@bot.listen()
async def on_message(message: Message):
    if message.content.startswith('!cocoa-count'):
        return
    if VERBOSE:
        print('-----------------------------')
        print("New message!")
        print(f'from {message.author.id}')
        print(message.content)
    num_of_cocoas_in_message = len(COCOA_REGEX.findall(message.content))
    if VERBOSE:
        print(f"Message has {num_of_cocoas_in_message} cocoas")
    user_id = message.author.id
    current_cocoa_count = get_cocoa_count_by_id(user_id)
    new_cocoa_count = current_cocoa_count + num_of_cocoas_in_message

    conn = sqlite3.connect(COCOA_DB)
    c = conn.cursor()
    c.execute(f'UPDATE {COCOA_TABLE} SET count={new_cocoa_count} WHERE user_id={user_id}')
    conn.commit()
    conn.close()


def get_cocoa_count_by_id(user_id: int):
    conn = sqlite3.connect(COCOA_DB)
    c = conn.cursor()
    c.execute(f"SELECT count FROM {COCOA_TABLE} WHERE user_id={user_id}")
    cocoa_count = c.fetchone()[0]
    conn.close()
    return cocoa_count


def get_display_name_by_id(bot: commands.Bot, user_id: int):
    for member in bot.guilds.pop().members:
        if member.id == user_id:
            return member.display_name
    raise ValueError(f'User {user_id} is not a valid member id in this guild.')


def get_id_by_display_name(bot: commands.Bot, display_name: str):
    for member in bot.guilds.pop().members:
        if member.display_name is display_name:
            return member.id
    raise ValueError(f'User {display_name} is not a valid display name in this guild.')


def get_weekday_and_hms():
    weekday = datetime.datetime.today().weekday()
    hour = datetime.datetime.today().hour
    minute = datetime.datetime.today().minute
    second = datetime.datetime.today().second
    return weekday, hour, minute, second


def print_database(database, table):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    print('Printing SQLite DB')
    for row in c.execute(f'SELECT * FROM {table}'):
        print(row)
    print('Done printing SQLite DB')
    conn.close()


if __name__ == '__main__':
    TOKEN = os.getenv('COCOA_BOT_TOKEN')

    try:
        cocoa_db_uri = f'file:{pathname2url(COCOA_DB)}?mode=rw'
        conn = sqlite3.connect(cocoa_db_uri, uri=True)
        conn.close()
    except sqlite3.OperationalError:
        cocoa_db_uri = f'file:{pathname2url(COCOA_DB)}?mode=rwc'
        conn = sqlite3.connect(cocoa_db_uri, uri=True)
        c = conn.cursor()
        c.execute(f'CREATE TABLE {COCOA_TABLE} (id int, count int)')
        conn.commit()
        conn.close()

    bot.run(TOKEN)
