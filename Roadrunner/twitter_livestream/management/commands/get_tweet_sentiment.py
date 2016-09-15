from django.core.management.base import BaseCommand, CommandError
from ...models import Tweet, TUser, Hashtag, Media, URL, Track, TweetQueue
import indicoio
from django.conf import settings
from ._get_access_token import get_access_token
from twitter import Api
import json
from datetime import datetime

indicoio.config.api_key = settings.INDICO_KEY

class Command(BaseCommand):
    help = "Stream tweets into queue"

    def add_arguments(self, parser):
        parser.add_argument('tweet_id', nargs='+')

    def handle(self, *args, **options):

        tweet = Tweet.objects.get(id=options['tweet_id'][0])

        score = indicoio.sentiment_hq(tweet.text)
        tweet.sentiment_score = score
        tweet.save()
        self.stdout.write(str(score))
        return