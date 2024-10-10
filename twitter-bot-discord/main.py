import tweepy
from utils.processor import Processor
from config import config
from utils.converter import Converter
from utils.startup import pprint


class MyStream(tweepy.StreamingClient):
    def __init__(self, bearer_token, config_discord):
        super().__init__(bearer_token)
        self.config_discord = config_discord

    def _on_status(self, tweet):
        data = tweet.data
        for discord in self.config_discord:
            p = Processor(tweet=data, config=discord)

            if not (p.worth_follow() or p.worth_track() or p.worth_posting()):
                continue
            if not p.keyword_set_present() or p.blackword_set_present():
                continue

            for url in discord.get('urls', []):
                p.create_embed()
                p.attach_field()
                p.send_message(url)
                pprint(f"Tweet sent: {tweet['author_id']}")

    def on_tweet(self, tweet):
        try:
            self._on_status(tweet)
        except Exception as e:
            pprint(f"Error processing tweet: {e}")

# Load config and initialize stream
bearer_token = config['twitter']['bearer_token']
discord_config = config['Discord']

my_stream = MyStream(bearer_token, discord_config)
my_stream.add_rules(tweepy.StreamRule("Python OR Tweepy"))
my_stream.filter()
