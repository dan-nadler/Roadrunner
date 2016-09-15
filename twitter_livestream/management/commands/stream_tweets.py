from django.core.management.base import BaseCommand, CommandError
from ...models import Tweet, TUser, Hashtag, Media, URL, Track, TweetQueue
from django.conf import settings
from ._get_access_token import get_access_token
from twitter import Api
import json
from datetime import datetime

class Command(BaseCommand):
    help = "Stream tweets into queue"

    def add_arguments(self, parser):
        parser.add_argument('track', nargs='+')

    def handle(self, *args, **options):
        track = options['track']
        tracks = [Track.objects.get_or_create(text=t)[0] for t in track]

        CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
        CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET
        ACCESS_TOKEN = '2163588176-vrKoKmhLRwanWjEXUw7Zx6KhMMZrEy7jGa1MH3S'
        ACCESS_TOKEN_SECRET = 'asQYfiYM4YermUgoswAdkCjcSDS31kwji8APRZ18Zgu57'
        # ACCESS_TOKEN, ACCESS_TOKEN_SECRET = get_access_token(CONSUMER_KEY, CONSUMER_SECRET)

        api = Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        iterator = api.GetStreamFilter(track=track)

        self.stdout.write('Streaming...', ending='\r')
        i = 0
        for tweet in iterator:
            i += 1
            q = TweetQueue(json=json.dumps(tweet), tracks=','.join(track))
            q.save()
            self.stdout.write('Streaming...{0}'.format(str(i)), ending='\r')
