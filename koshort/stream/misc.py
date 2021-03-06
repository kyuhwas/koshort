from time import sleep
from koshort.stream import BaseStreamer, TwitterStreamer
from koshort.stream.naver import get_current_trend


class NavtterStreamer(BaseStreamer):
    """Start streaming of twitter about naver's current top trending keywords. 
    In order to use NavtterStreamer, you have to set-up both twitter and Navtter's options.

    .. code-block:: python

        from koshort.stream import NavtterStreamer

        app = NavtterStreamer()
        app.show_options()  # Print available options
        app.options.interval = 3600  # Update naver trends every 3600 secs
        app.options.verbose = True  # Print trends

        # Your twitter api keys and tokens.
        app.twitter.options.consumer_key = 'consumer_key'
        app.twitter.options.consumer_secret = 'consumer_secret'
        app.twitter.options.access_token = 'access_token'
        app.twitter.options.access_token_secret = 'access_token_secret'

        # Filter retweets to prevent potential repetition.
        app.twitter.options.filter_retweets = True

        # Print tweets.
        app.twitter.options.verbose = True
        app.stream()

    """

    def __init__(self, is_async=True):
        self.is_async = is_async

        parser = self.get_parser()
        parser.add_argument(
            '-i', '--interval', 
            help="streaming interval(secs)", 
            default=100,
            type=int
        )
        self.options, _ = parser.parse_known_args()
        self.twitter  = TwitterStreamer()
        self.trend = None
        self.streamer = None

    def get_trend(self):
        _, self.trend = get_current_trend()
        if self.options.verbose:
            print(self.trend)

    def job(self):
        self.get_trend()
        twitter = TwitterStreamer(word_list=self.trend, is_async=False)
        twitter.options = self.twitter.options
        twitter.options.time_limits = self.options.interval
        twitter.create_listener()
        twitter.job()
        self.job()
