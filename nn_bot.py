import urllib.request
import urllib.error
import json

import discord
from discord.ext import commands

startup_extensions = ["cogs.hearthstone", "cogs.twitter"]

description = '''thababn'''
bot = commands.Bot(command_prefix='.', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

@bot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

#@bot.listen('on_message')
#async def scrape_tweet(message):
#    tweet = re.match(r'https?://(mobile.)?twitter.com/(#!/)?([_0-9a-zA-Z]+)/status/(?P<id>\d+)', message.content)
#    if tweet:
#        if bot.fetch_key("twitter_consumer") and bot.fetch_key("twitter_consumer_secret") and bot.fetch_key("twitter_access") and bot.fetch_key("twitter_access_secret"):
#            status = twitter_api.get_status(tweet.group('id'))
#            media = status._json['extended_entities']['media']
#            strout = ""
#            for m in media:
#                strout += m['media_url'] + " "
#            await bot.send_message(message.channel, strout)
#        else:
#            await bot.send_message("error: missing twitter API key")
#            return
def start():
        try:
            json_file = open('config', 'r')
            json_data = json.load(json_file)
            key = json_data["keys"]["discord"]
        except IOError as e:
            print("error: can't read config file")
        if key:
            bot.run(key)
        else:
            print("error: missing discord API key")

start()