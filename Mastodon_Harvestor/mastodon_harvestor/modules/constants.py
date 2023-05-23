import os

MASTODON_SITES = [
    {
        'URL': 'https://mastodon.social',
        'TOKEN': 'MASTODON_ACCESS_TOKEN_SOCIAL'
    },
    {
        'URL': 'https://mastodon.au',
        'TOKEN': 'MASTODON_ACCESS_TOKEN_AU'
    },
    {
        'URL': 'https://mastodon.cloud',
        'TOKEN': 'MASTODON_ACCESS_TOKEN_CLOUD'
    }
]
TAGS = [
    'health',
    'healthcare',
    'cancer'
]
SEARCH_LIMIT = 300
# DB_URL='http://127.0.0.1:5984/'
# DB_URL='http://172.26.134.93:5984/'
# DB_USERNAME='admin'
# DB_PASSWORD='admin'
DB_URL=os.environ['DB_URL']
DB_USERNAME=os.environ['DB_USERNAME']
DB_PASSWORD=os.environ['DB_PASSWORD']
TOOTH_DATABASE='mastodon_tooth'
TOKEN_DATABASE='mastodon_token'

MAX_ATTEMPT=10