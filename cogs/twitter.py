import discord
from discord.ext import commands
import tweepy
import json
import re

class Twitter:
    """Twitter utilities."""
    
    keys_set = False
    twitter_api = None
    
    def __init__(self, bot):
        self.bot = bot;
        try:
            json_file = open('config', 'r')
            json_data = json.load(json_file)
            key_consumer = json_data["keys"]["twitter_consumer"]
            key_consumer_s = json_data["keys"]["twitter_consumer_secret"]
            key_access = json_data["keys"]["twitter_access"]
            key_access_s = json_data["keys"]["twitter_access_secret"]
            if key_consumer and key_consumer_s and key_access and key_access_s:
                self.keys_set = True
            
            twitter_auth = tweepy.OAuthHandler(key_consumer, key_consumer_s)
            twitter_auth.set_access_token(key_access, key_access_s)
            self.twitter_api = tweepy.API(twitter_auth)
        except IOError as e:
            print("error: can't read config file")

    async def scrape_tweet(self, message):
        tweet = re.match(r'https?://(mobile.)?twitter.com/(#!/)?([_0-9a-zA-Z]+)/status/(?P<id>\d+)', message.content)
        if tweet:
            if self.keys_set:
                status = self.twitter_api.get_status(tweet.group('id'))
            
                #Check for TTS
                tts = False
                if ".tts" in message.content:
                    tts = True
                    
                #Scrape images/videos
                strout2 = ""
                if 'extended_entities' in status._json:
                    media = status._json['extended_entities']['media']
                    for m in media:
                        if m['type'] == 'photo': #This is an image. Pull it out directly.
                            strout2 += m['media_url'] + " "
                        if m['type'] == 'video' or m['type'] == 'animated_gif': #This is a video. Pull the first MP4 you can find out.
                            for variant in m['video_info']['variants']:
                                if variant['content_type'] == 'video/mp4':
                                    strout2 += variant['url'] + " "
                                    break;
                
                #Print what we want/found
                if tts:
                    strout1 = re.sub(r'https?:\/\/[^\s]*', ' ', status.text)
                    await self.bot.send_message(message.channel, strout1, tts=True)
                if strout2 != "":
                    await self.bot.send_message(message.channel, strout2)
            else:
                await self.bot.send_message("error: missing twitter API key")
                return
            
def setup(bot):
    b = Twitter(bot)
    bot.add_listener(b.scrape_tweet, "on_message")
    bot.add_cog(b)