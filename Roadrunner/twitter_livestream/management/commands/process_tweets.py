from django.core.management.base import BaseCommand, CommandError
from ...models import Tweet, TUser, Hashtag, Media, URL, Track, TweetQueue
from django.conf import settings
from ._get_access_token import get_access_token
from twitter import Api
import json
from datetime import datetime


class Command(BaseCommand):
    help = "Process tweets into database"

    def handle(self, *args, **options):

        while TweetQueue.objects.count() > 0:
            try:
                del tweet
                del q
                del track_list
                del user_list
                del user
            except:
                pass

            q = TweetQueue.objects.first()
            tweet = json.loads(q.json)
            track_list = q.tracks.split(',')
            tracks = [Track.objects.get_or_create(text=t)[0] for t in track_list]

            if 'user' not in tweet:
                q.delete()
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

            q.delete()

            self.stdout.write('{0} tweets remaining.'.format(str(TweetQueue.objects.count())), ending='\r')
