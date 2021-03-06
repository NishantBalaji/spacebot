import os
import json
from discord.ext import commands
from dotenv import load_dotenv
import random
import http.client
from nasapy.api import *

load_dotenv()
KEY = os.getenv('API_KEY')
TOKEN = os.getenv('DISCORD_TOKEN')
NASA_KEY = os.getenv('NASA_KEY')

nasa = Nasa(key = NASA_KEY)
bot = commands.Bot(command_prefix='!', case_insensitive = True)
print(nasa.limit_remaining)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='hi')
async def test(ctx):

    await ctx.send("hello")

# Repeat a user's message back to them
@bot.command(name='echo')
async def echo(ctx, *args):
    if not args:
        await ctx.send("What you want me to say? (syntax `!echo [input]`)")
    else:
        output = " "
        for words in args:
            output += words
            output += " "
        await ctx.message.delete()
        await ctx.send(output)


@bot.command(name='apod', help='Responds with NASA\'s picture of the day. Put the date after the command as `YYYY MM DD` to specify a date.')
async def apod(ctx, *args):
    if not args:
        pic = nasa.picture_of_the_day(hd = True)
    else:
        date = []
        for words in args:
            date.append(words)
        if len(date) == 3:
            year = date[0]
            month = date[1]
            day = date[2]
            try:
                pic = nasa.picture_of_the_day(year + '-' + month + '-' + day, hd=True)
            except:
                await ctx.send("Invalid Request.")
        else:
            await ctx.send('Not a valid input, date must be in `YYYY MM DD` and must be a previous date.')
            return 0

    if 'copyright' in pic:
        await ctx.send('Title: ' + pic['title'] + '\n' + 'Author: ' + pic['copyright'] + '\n' + 'Date: ' + pic['date'])
    else:
        await ctx.send('Title: ' + pic['title'] + '\n' + 'Date: ' + pic['date'])
    await ctx.send(pic['hdurl'])
    await ctx.send('>>> ' + '*' + pic['explanation'] + '*')

@bot.command(name = 'epic')
async def epicImg(ctx, *args):
    date = []
    for words in args:
        date.append(words)
    if len(date) == 3:
        year = date[0]
        month = date[1]
        day = date[2]

    e = nasa.epic(date=year + '-' + month + '-' + day)

    s = e[3]
    await ctx.send('https://epic.gsfc.nasa.gov/archive/natural/' + year + '/' + month + '/' + day + '/png/'+ str(s['image']) + '.png')

#@bot.command(name='')
#@bot.command(name='help')
#async def help(ctx):


bot.run(TOKEN)
