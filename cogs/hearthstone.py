import discord
from discord.ext import commands
import re
import urllib.request
import urllib.error
import json

class Hearthstone:
    """Hearthstone utilities."""
    
    key = None
    def __init__(self, bot):
        self.bot = bot;
        try:
            json_file = open('config', 'r')
            json_data = json.load(json_file)
            self.key = json_data["keys"]["mashape"]
        except IOError as e:
            print("error: can't read config file")

    @commands.command()
    async def hs(self, name : str):
        if self.key != None:
            try:
                request = urllib.request.Request("https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + name + "?collectible=1", headers={"X-Mashape-Key": self.key})
                response = urllib.request.urlopen(request)
                await self.bot.say(json.loads(response.read().decode("utf-8"))[0]['img'])
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    await self.bot.say("Unknown card")
                else:
                    await self.bot.say("Error: Code " + str(e.code))
        else:
            await self.bot.say("Error: missing Hearthstone API key")

def setup(b):
    b.add_cog(Hearthstone(b))