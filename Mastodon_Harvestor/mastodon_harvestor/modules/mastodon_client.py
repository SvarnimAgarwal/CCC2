from mastodon import Mastodon
from ibmcloudant.cloudant_v1 import BulkDocs
from modules.mastodon_stream_listenr import MastodonStreamListener
from modules.mastodon_tooth import Tooth
from modules.constants import *
from bs4 import BeautifulSoup
import re
import emoji

class MastodonClient():

    def __init__(self, url, token, db_client) -> None:
        print(f'MastodonClient Created for {url}')
        self._mastodon = Mastodon(
            api_base_url=url,
            access_token=token
        )
        self._stream_listner = MastodonStreamListener(self)
        self.db_client = db_client
        self.stream = None
        self._tooth_docs = []

    def start_public_streaming(self) -> None:
        print('Public Streaming Started')
        self.stream = self._mastodon.stream_public(self._stream_listner)
    
    def close_stream(self) -> None:
        print('Closed streaming')
        self.stream.close()

    def start_hashtag_streaming(self) -> None:
        for tag in TAGS:
            print(f'HashTag Streaming Started with {tag}')
            self._mastodon.stream_hashtag(tag, self._stream_listner)

    def get_past_tooth(self) -> None:
        for tag in TAGS:
            # query = f'#{tag}'
            result = self._mastodon.timeline_hashtag(tag, limit=SEARCH_LIMIT)
            # print(result)
            print(len(result))
            # break

    def on_update_callback(self, status) -> None:
        # Add status to database which has tags and written in english
        if (self._valid_status(status)):
            tooth = self._parse_status(status)
            self._add_tooth_to_database(tooth)

    def _valid_status(self, status) -> bool:
        if (len(status['tags']) == 0):
            return False
        return True

    def _parse_status(self, status) -> Tooth:
        id = status['id']
        created_date = str(status['created_at'])
        language = status['language']
        hashtags = [tag['name'] for tag in status['tags']]
        content = self._parse_content(status['content']).lower()
        return Tooth(id, created_date, language, hashtags, content)

    def _parse_content(self, content) -> str:
        string = BeautifulSoup(content, 'html.parser').get_text()

        # remove URLs
        url_pattern = re.compile(r"https?://\S+")
        string = url_pattern.sub("", string)

        # remove emojis
        string = emoji.replace_emoji(string, replace='')

        # remove mentions
        mention_pattern = re.compile(r"@[\w]+")
        string = mention_pattern.sub("", string)

        # remove #
        string = string.replace('#', '')

        return string
    
    def _add_tooth_to_database(self, tooth) -> None:
        response = self.db_client.add_document(TOOTH_DATABASE, tooth.to_document())
        print(response)

