from django.core.management.base import BaseCommand, CommandError
from ...models import Tweet, TUser, Hashtag, Media, URL
from django.conf import settings
from twitter import oauth_dance, read_token_file, TwitterStream, OAuth
import os
from datetime import datetime

class Command(BaseCommand):
    help = "Stream tweets into database"

    def add_arguments(self, parser):
        parser.add_argument('track', nargs='+')

    def handle(self, *args, **options):
        track = ','.join(options['track'])

        CONSUMER_KEY = settings.TWITTER_CONSUMER_KEY
        CONSUMER_SECRET = settings.TWITTER_CONSUMER_SECRET

        MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')
        if not os.path.exists(MY_TWITTER_CREDS):
            oauth_dance("SentimentVisualizer", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

        oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
        twitter_stream = TwitterStream(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

        iterartor = twitter_stream.statuses.filter(track=track)

        print('Streaming...', end='\r')
        i = 0
        for tweet in iterartor:
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
            print('Streaming...{0}'.format(str(i)), end='\r')
