from django.db import models

# Create your models here.
class TUser(models.Model):

    screen_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)

    favorites_count = models.BigIntegerField()
    followers_count = models.BigIntegerField()
    friends_count = models.BigIntegerField()
    twitter_id = models.BigIntegerField()
    statuses_count = models.BigIntegerField()

    created_at = models.DateTimeField()

    time_zone = models.CharField(max_length=250, null=True)
    lang = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=250, null=True)


class Hashtag(models.Model):

    text = models.CharField(max_length=250)


class Media(models.Model):

    url = models.URLField()
    display_url = models.URLField()
    media_url = models.URLField()
    type = models.CharField(max_length=250)


class URL(models.Model):

    url = models.URLField()
    display_url = models.URLField()
    expanded_url = models.URLField()


class Track(models.Model):
    text = models.CharField(max_length=250, unique=True)


class Tweet(models.Model):
    hashtags = models.ManyToManyField(Hashtag)
    media = models.ManyToManyField(Media)
    # symbols = models.ManyToManyField()
    urls = models.ManyToManyField(URL)
    user_mentions = models.ManyToManyField(TUser, related_name='mentions')

    created_at = models.DateTimeField()
    favorite_count = models.BigIntegerField()
    twitter_id = models.BigIntegerField()

    in_reply_to_screen_name = models.CharField(max_length=250, null=True)
    in_reply_to_user_id = models.BigIntegerField(null=True)

    is_quote_status = models.BooleanField()
    retweet_count = models.BigIntegerField()
    retweeted = models.BooleanField()

    text = models.CharField(max_length=250)
    timestamp_ms = models.BigIntegerField()
    user = models.ForeignKey(TUser, related_name='tweets')
    lang = models.CharField(max_length=10)

    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)

    track = models.ManyToManyField(Track)

    sentiment_score = models.FloatField(blank=True, null=True)


class TweetQueue(models.Model):
    json = models.TextField()
    tracks = models.TextField()
