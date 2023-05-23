from mastodon import StreamListener

class MastodonStreamListener(StreamListener):
    
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client

    def on_update(self, status):
        self.client.on_update_callback(status)

    def on_abort(self, err):
        return super().on_abort(err)
