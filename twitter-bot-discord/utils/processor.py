import requests


class Processor:
    def __init__(self, tweet, config):
        self.embed = None
        self.tweet = tweet
        self.config = config

    def worth_follow(self):
        # Check if tweet is from followed users
        return self.tweet.get('author_id') in self.config.get('followed_users', [])

    def worth_track(self):
        # Check if the tweet contains tracked keywords
        return any(keyword in self.tweet.get('text', '').lower() for keyword in self.config.get('tracked_keywords', []))

    def worth_posting(self):
        # Check for specific conditions
        return 'ltion' in self.tweet.get('text', '').lower()

    def keyword_set_present(self):
        # Check if tweet contains at least one keyword from the config
        return any(keyword in self.tweet.get('text', '').lower() for keyword in self.config.get('keywords', []))

    def blackword_set_present(self):
        # Ensure tweet doesn't contain blacklisted words
        return any(blackword in self.tweet.get('text', '').lower() for blackword in self.config.get('blackwords', []))

    def create_embed(self, title):
        # Create an embedded message for Discord
        self.embed = {'title': title, 'description': self.tweet.get('text')}

    def attach_field(self, name):
        # Attach additional info fields to the embed
        self.embed['fields'] = [{'name': name, 'value': self.tweet.get('author_id')}]

    def send_message(self, url):
        # Send message to Discord webhook
        requests.post(url, json=self.embed)
