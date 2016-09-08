from django.core.management.base import BaseCommand, CommandError
from ...models import Tweet, TUser, Hashtag, Media, URL, Track
from django.conf import settings
from ._get_access_token import get_access_token
from twitter import Api
import os
from datetime import datetime

class Command(BaseCommand):
    help = "Stream tweets into database"

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

        print('Streaming...', end='\r')
        i = 0
        for tweet in iterator:
            i+=1
            if 'user' not in tweet:
                continue
            user_list = TUser.objects.filter(twitter_id=tweet['user']['id'])
            if user_list.count() == 0:
                new_user = TUser(
                    twitter_id=tweet['user']['id'],
                    screen_name=tweet['user']['screen_name'],
                    statuses_count=tweet['user']['statuses_count'],
                    favorites_count=tweet['user']['favourites_count'],
                    followers_count=tweet['user']['followers_count'],
                    friends_count=tweet['user']['friends_count'],
                    name=tweet['user']['name'],
                    created_at=datetime.strptime(tweet['user']['created_at'], '%a %b %d %H:%M:%S %z %Y'),
                    lang=tweet['user']['lang'],
                    time_zone=tweet['user']['time_zone'],
                    location=tweet['user']['location'],
                )
                new_user.save()

                user_list = TUser.objects.filter(twitter_id=tweet['user']['id'])

            if user_list.count() == 1:
                user = user_list.all()[0]

            retweeted = False
            retweet_count = 0

            if 'retweeted_status' in tweet:
                if tweet['retweeted_status'] is not None:
                    retweeted = True
                    retweet_count = tweet['retweeted_status']['retweet_count']

            lat, lon = None, None
            if tweet['coordinates'] is not None:
                lat, lon = tweet['coordinates']['coordinates']

            new_tweet = Tweet(
                created_at=datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y'),
                favorite_count=tweet['favorite_count'],
                twitter_id=tweet['id'],
                lat=lat,
                lon=lon,

                in_reply_to_screen_name=tweet['in_reply_to_screen_name'],
                in_reply_to_user_id=tweet['in_reply_to_user_id'],

                is_quote_status=tweet['is_quote_status'],
                retweet_count=retweet_count,
                retweeted=retweeted,

                text=tweet['text'],
                timestamp_ms=tweet['timestamp_ms'],
                user=user,
                lang=tweet['lang'],
            )

            new_tweet.save()

            for t in tracks:
                new_tweet.track.add(t)

            print('Streaming... {0}'.format(str(i)), end='\r')
