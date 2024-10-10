import tweepy
import yaml

# Authenticate using Bearer Token (Twitter API v2)
bearer_token = "your_bearer_token"
client = tweepy.Client(bearer_token)

# Example: Fetch Twitter user ID from username
def get_user_id(username):
    response = client.get_user(username=username)
    return response.data.id if response.data else None

# Get user IDs dynamically
followed_users = [
    get_user_id('TwitterUsername1'),
    get_user_id('TwitterUsername2')
]

# Update YAML config with dynamic user IDs
config_data = {
    'twitter': {
        'bearer_token': bearer_token
    },
    'Discord': [
        {
            'name': 'Channel 1',
            'followed_users': followed_users,
            'tracked_keywords': ['Python', 'Tweepy'],
            'keywords': ['Python', 'Code'],
            'blackwords': ['spam'],
            'urls': ['https://discordapp.com/api/webhooks/your_webhook_url']
        }
    ]
}

# Save updated config to YAML
save_to_yaml('config.yml', config_data)
