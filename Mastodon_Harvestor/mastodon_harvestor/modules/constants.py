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
    },
    {
        'URL': 'https://mastodon.world',
        'TOKEN': 'MASTODON_ACCESS_TOKEN_WORLD'
    },
    {
        'URL': 'https://mastodonapp.uk',
        'TOKEN': 'MASTODON_ACCESS_TOKEN_UK'
    }
]
SEARCH_LIMIT = 300
DB_URL=os.environ['DB_URL']
DB_USERNAME=os.environ['DB_USERNAME']
DB_PASSWORD=os.environ['DB_PASSWORD']
TOOTH_DATABASE='mastodon_tooth'
TOKEN_DATABASE='mastodon_token'

MAX_ATTEMPT=10
